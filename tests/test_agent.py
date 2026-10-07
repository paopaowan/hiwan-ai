from hiwan_ai.agent import AgentContext, AllowAllPolicy, MinimalAgent
from hiwan_ai.llm import LLMResponse
from hiwan_ai.tools import LocalSystemInfoTool


def response(content: str) -> LLMResponse:
    return LLMResponse(
        content=content,
        thinking="",
        done_reason="stop",
        prompt_eval_count=1,
        prompt_eval_duration_ns=1,
        eval_count=1,
        eval_duration_ns=1,
    )


class FakeLLM:
    def __init__(self, outputs: list[str]) -> None:
        self.outputs = list(outputs)
        self.calls = []

    def chat(self, messages, **kwargs) -> LLMResponse:
        self.calls.append((messages, kwargs))
        return response(self.outputs.pop(0))


class DenyAllPolicy:
    def allows(self, *, identity: str, action: str) -> bool:
        return False


def test_agent_without_tools_calls_llm_once() -> None:
    llm = FakeLLM(["HIWAN_AGENT_OK"])
    agent = MinimalAgent(llm)

    result = agent.run("hello", context=AgentContext(identity="richard"))

    assert result.identity == "richard"
    assert result.content == "HIWAN_AGENT_OK"
    assert result.tool_used is None
    assert len(llm.calls) == 1


def test_agent_executes_selected_tool_and_finishes() -> None:
    llm = FakeLLM(
        [
            '{"action":"tool","tool":"local_system_info","arguments":{}}',
            "The machine architecture is arm64.",
        ]
    )
    agent = MinimalAgent(llm, tools=[LocalSystemInfoTool()])

    result = agent.run(
        "What architecture is this machine?",
        context=AgentContext(identity="richard"),
    )

    assert result.tool_used == "local_system_info"
    assert "architecture=" in (result.tool_result or "")
    assert result.content == "The machine architecture is arm64."
    assert len(llm.calls) == 2


def test_policy_boundary_can_deny_before_llm() -> None:
    llm = FakeLLM(["unused"])
    agent = MinimalAgent(llm, policy=DenyAllPolicy())

    try:
        agent.run("hello", context=AgentContext(identity="richard"))
    except PermissionError:
        pass
    else:
        raise AssertionError("expected PermissionError")

    assert llm.calls == []


def test_empty_prompt_is_rejected() -> None:
    agent = MinimalAgent(FakeLLM(["unused"]), policy=AllowAllPolicy())

    try:
        agent.run("   ")
    except ValueError:
        pass
    else:
        raise AssertionError("expected ValueError")
