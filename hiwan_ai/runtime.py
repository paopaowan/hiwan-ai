from __future__ import annotations

from dataclasses import dataclass

from .agent import AgentContext, AgentResult, MinimalAgent
from .storage import SQLiteRunStore


@dataclass(frozen=True)
class RuntimeResult:
    run_id: int
    agent_result: AgentResult


class HiwanRuntime:
    """Minimal Phase 1 tracer-bullet runtime.

    Flow:
        prompt
          -> Agent
          -> Identity / Policy
          -> optional Tool
          -> LLM final answer
          -> SQLite persistence
    """

    def __init__(self, *, agent: MinimalAgent, store: SQLiteRunStore) -> None:
        self.agent = agent
        self.store = store

    def run(
        self,
        prompt: str,
        *,
        context: AgentContext | None = None,
    ) -> RuntimeResult:
        context = context or AgentContext()

        result = self.agent.run(prompt, context=context)

        run_id = self.store.record_run(
            identity=result.identity,
            prompt=prompt,
            response=result.content,
            tool_used=result.tool_used,
            tool_result=result.tool_result,
            status="ok",
        )

        return RuntimeResult(
            run_id=run_id,
            agent_result=result,
        )
