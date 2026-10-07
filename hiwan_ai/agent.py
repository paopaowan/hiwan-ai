from __future__ import annotations

from dataclasses import dataclass
import json
from typing import Protocol

from .llm import LLMResponse
from .tools import Tool


class LLMClient(Protocol):
    def chat(self, messages, **kwargs) -> LLMResponse: ...


@dataclass(frozen=True)
class AgentContext:
    identity: str = "richard"


@dataclass(frozen=True)
class AgentResult:
    identity: str
    content: str
    done_reason: str | None
    tool_used: str | None = None
    tool_result: str | None = None


class AllowAllPolicy:
    """Phase 1 policy placeholder."""

    def allows(self, *, identity: str, action: str) -> bool:
        return True


class MinimalAgent:
    """Phase 1 minimal agent with one optional local tool.

    Flow:
        prompt
          -> identity
          -> policy
          -> LLM tool decision
          -> optional local tool
          -> LLM final answer
    """

    def __init__(
        self,
        llm: LLMClient,
        *,
        tools: list[Tool] | None = None,
        policy: AllowAllPolicy | None = None,
    ) -> None:
        self.llm = llm
        self.policy = policy or AllowAllPolicy()
        self.tools = {tool.name: tool for tool in (tools or [])}

    def _llm_chat(self, messages, *, num_predict: int = 256) -> LLMResponse:
        return self.llm.chat(
            messages,
            think=False,
            temperature=0.0,
            num_ctx=8192,
            num_predict=num_predict,
            keep_alive="10m",
        )

    def run(self, prompt: str, *, context: AgentContext | None = None) -> AgentResult:
        context = context or AgentContext()

        if not prompt.strip():
            raise ValueError("prompt must not be empty")

        if not self.policy.allows(identity=context.identity, action="agent.run"):
            raise PermissionError(
                f"policy denied agent.run for identity={context.identity!r}"
            )

        if not self.tools:
            response = self._llm_chat([{"role": "user", "content": prompt}])
            return AgentResult(
                identity=context.identity,
                content=response.content,
                done_reason=response.done_reason,
            )

        tool_catalog = "\n".join(
            f"- {tool.name}: {tool.description}" for tool in self.tools.values()
        )

        decision_prompt = f"""You are a tool router.

Available tools:
{tool_catalog}

User request:
{prompt}

Return JSON only.

If a tool is required:
{{"action":"tool","tool":"TOOL_NAME","arguments":{{}}}}

If no tool is required:
{{"action":"answer","answer":"YOUR_FINAL_ANSWER"}}
"""

        decision_response = self._llm_chat(
            [{"role": "user", "content": decision_prompt}],
            num_predict=128,
        )

        try:
            decision = json.loads(decision_response.content.strip())
        except json.JSONDecodeError as exc:
            raise RuntimeError(
                f"tool router returned invalid JSON: {decision_response.content!r}"
            ) from exc

        action = decision.get("action")

        if action == "answer":
            return AgentResult(
                identity=context.identity,
                content=str(decision.get("answer") or ""),
                done_reason=decision_response.done_reason,
            )

        if action != "tool":
            raise RuntimeError(f"unsupported tool-router action: {action!r}")

        tool_name = decision.get("tool")
        tool = self.tools.get(tool_name)
        if tool is None:
            raise RuntimeError(f"unknown tool requested: {tool_name!r}")

        if not self.policy.allows(
            identity=context.identity,
            action=f"tool.{tool_name}",
        ):
            raise PermissionError(
                f"policy denied tool.{tool_name} for identity={context.identity!r}"
            )

        arguments = decision.get("arguments") or {}
        if not isinstance(arguments, dict):
            raise RuntimeError("tool arguments must be a JSON object")

        tool_result = tool.run(arguments)

        final_response = self._llm_chat(
            [
                {
                    "role": "user",
                    "content": (
                        f"Original user request:\n{prompt}\n\n"
                        f"Tool used: {tool_name}\n"
                        f"Tool result:\n{tool_result}\n\n"
                        "Answer the original request using only the tool result. "
                        "Be concise."
                    ),
                }
            ],
            num_predict=128,
        )

        return AgentResult(
            identity=context.identity,
            content=final_response.content,
            done_reason=final_response.done_reason,
            tool_used=tool_name,
            tool_result=tool_result,
        )
