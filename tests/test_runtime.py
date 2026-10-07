from pathlib import Path

from hiwan_ai.agent import AgentContext, AgentResult
from hiwan_ai.runtime import HiwanRuntime
from hiwan_ai.storage import SQLiteRunStore


class FakeAgent:
    def run(self, prompt: str, *, context: AgentContext | None = None) -> AgentResult:
        context = context or AgentContext()
        return AgentResult(
            identity=context.identity,
            content="The machine architecture is arm64.",
            done_reason="stop",
            tool_used="local_system_info",
            tool_result="os=Darwin release=test architecture=arm64",
        )


def test_runtime_persists_agent_result(tmp_path: Path) -> None:
    store = SQLiteRunStore(tmp_path / "runtime.db")
    runtime = HiwanRuntime(agent=FakeAgent(), store=store)

    result = runtime.run(
        "What architecture is this machine?",
        context=AgentContext(identity="richard"),
    )

    saved = store.get_run(result.run_id)

    assert saved is not None
    assert saved.identity == "richard"
    assert saved.prompt == "What architecture is this machine?"
    assert saved.response == "The machine architecture is arm64."
    assert saved.tool_used == "local_system_info"
    assert saved.tool_result == "os=Darwin release=test architecture=arm64"
    assert saved.status == "ok"
    assert store.count_runs() == 1
