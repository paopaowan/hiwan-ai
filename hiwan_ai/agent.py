from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

from .llm import LLMResponse


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


class AllowAllPolicy:
    """Phase 1 policy placeholder.

    This preserves the Identity -> Policy boundary without introducing
    a real authorization framework yet.
    """

    def allows(self, *, identity: str, action: str) -> bool:
        return True


class MinimalAgent:
    """Phase 1 minimal agent loop.

    Flow:
        prompt
          -> identity
          -> policy
          -> LLM
          -> result

    Tools are intentionally not part of Phase 1D. They arrive in Phase 1E.
    """

    def __init__(self, llm: LLMClient, policy: AllowAllPolicy | None = None) -> None:
        self.llm = llm
        self.policy = policy or AllowAllPolicy()

    def run(self, prompt: str, *, context: AgentContext | None = None) -> AgentResult:
        context = context or AgentContext()

        if not prompt.strip():
            raise ValueError("prompt must not be empty")

        if not self.policy.allows(identity=context.identity, action="llm.chat"):
            raise PermissionError(
                f"policy denied llm.chat for identity={context.identity!r}"
            )

        response = self.llm.chat(
            [{"role": "user", "content": prompt}],
            think=False,
            temperature=0.0,
            num_ctx=8192,
            num_predict=256,
            keep_alive="10m",
        )

        return AgentResult(
            identity=context.identity,
            content=response.content,
            done_reason=response.done_reason,
        )
