from hiwan_ai.agent import AgentContext, AllowAllPolicy, MinimalAgent
from hiwan_ai.llm import LLMResponse


class FakeLLM:
    def __init__(self) -> None:
        self.calls = []

    def chat(self, messages, **kwargs) -> LLMResponse:
        self.calls.append((messages, kwargs))
        return LLMResponse(
            content="HIWAN_AGENT_OK",
            thinking="",
            done_reason="stop",
            prompt_eval_count=1,
            prompt_eval_duration_ns=1,
            eval_count=1,
            eval_duration_ns=1,
        )


class DenyAllPolicy:
    def allows(self, *, identity: str, action: str) -> bool:
        return False


def test_minimal_agent_preserves_identity_and_calls_llm() -> None:
    llm = FakeLLM()
    agent = MinimalAgent(llm)

    result = agent.run(
        "hello",
        context=AgentContext(identity="richard"),
    )

    assert result.identity == "richard"
    assert result.content == "HIWAN_AGENT_OK"

    messages, kwargs = llm.calls[0]
    assert messages == [{"role": "user", "content": "hello"}]
    assert kwargs["think"] is False
    assert kwargs["temperature"] == 0.0
    assert kwargs["num_ctx"] == 8192


def test_policy_boundary_can_deny() -> None:
    llm = FakeLLM()
    agent = MinimalAgent(llm, policy=DenyAllPolicy())

    try:
        agent.run("hello", context=AgentContext(identity="richard"))
    except PermissionError:
        pass
    else:
        raise AssertionError("expected PermissionError")

    assert llm.calls == []


def test_empty_prompt_is_rejected() -> None:
    agent = MinimalAgent(FakeLLM(), policy=AllowAllPolicy())

    try:
        agent.run("   ")
    except ValueError:
        pass
    else:
        raise AssertionError("expected ValueError")
