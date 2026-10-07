from pathlib import Path

from hiwan_ai.agent import AgentContext, MinimalAgent
from hiwan_ai.llm import OllamaClient
from hiwan_ai.runtime import HiwanRuntime
from hiwan_ai.storage import SQLiteRunStore
from hiwan_ai.tools import LocalSystemInfoTool


DB_PATH = Path.home() / ".hiwan" / "dev" / "databases" / "hiwan.db"


def main() -> int:
    store = SQLiteRunStore(DB_PATH)

    agent = MinimalAgent(
        OllamaClient(model="qwen3.5:27b-mlx"),
        tools=[LocalSystemInfoTool()],
    )

    runtime = HiwanRuntime(agent=agent, store=store)

    prompt = (
        "What CPU architecture is the machine running Hiwan AI on? "
        "Use the local_system_info tool and answer concisely."
    )

    before = store.count_runs()

    runtime_result = runtime.run(
        prompt,
        context=AgentContext(identity="richard"),
    )

    after = store.count_runs()
    saved = store.get_run(runtime_result.run_id)
    result = runtime_result.agent_result

    print("Database:", store.path)
    print("Run count before:", before)
    print("Run count after:", after)
    print("Run id:", runtime_result.run_id)
    print("Identity:", result.identity)
    print("Tool used:", result.tool_used)
    print("Tool result:", result.tool_result)
    print("Response:", repr(result.content.strip()))
    print("Persisted identity:", saved.identity if saved else None)
    print("Persisted tool:", saved.tool_used if saved else None)
    print("Persisted status:", saved.status if saved else None)

    repo_root = (Path.home() / "hiwan-ai").resolve()
    db_resolved = store.path.resolve()

    try:
        db_resolved.relative_to(repo_root)
        inside_repo = True
    except ValueError:
        inside_repo = False

    print("Database inside Git repo:", inside_repo)

    if after != before + 1:
        print("FAIL: run count did not increment exactly once")
        return 1

    if result.identity != "richard":
        print("FAIL: identity was not preserved")
        return 1

    if result.tool_used != "local_system_info":
        print("FAIL: expected local_system_info tool")
        return 1

    if "architecture=arm64" not in (result.tool_result or ""):
        print("FAIL: real tool result did not report arm64")
        return 1

    if saved is None:
        print("FAIL: persisted run could not be loaded")
        return 1

    if saved.prompt != prompt:
        print("FAIL: persisted prompt does not match")
        return 1

    if saved.response != result.content:
        print("FAIL: persisted response does not match")
        return 1

    if saved.tool_result != result.tool_result:
        print("FAIL: persisted tool result does not match")
        return 1

    if saved.status != "ok":
        print("FAIL: persisted status is not ok")
        return 1

    if inside_repo:
        print("FAIL: private runtime database is inside Git repository")
        return 1

    print("PASS: Phase 1G tracer bullet works end-to-end")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
