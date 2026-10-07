from pathlib import Path

from hiwan_ai.storage import SQLiteRunStore


EXPECTED_ROOT = Path.home() / ".hiwan" / "dev" / "databases"
DB_PATH = EXPECTED_ROOT / "hiwan.db"


def main() -> int:
    store = SQLiteRunStore(DB_PATH)

    run_id = store.record_run(
        identity="richard",
        prompt="Phase 1F synthetic persistence test",
        response="HIWAN_SQLITE_OK",
        tool_used="local_system_info",
        tool_result="architecture=arm64",
        status="ok",
    )

    record = store.get_run(run_id)

    print("Database:", store.path)
    print("Database exists:", store.path.exists())
    print("Run id:", run_id)
    print("Run count:", store.count_runs())
    print("Identity:", record.identity if record else None)
    print("Response:", repr(record.response) if record else None)
    print("Tool used:", record.tool_used if record else None)

    repo_root = (Path.home() / "hiwan-ai").resolve()
    db_resolved = store.path.resolve()

    try:
        db_resolved.relative_to(repo_root)
        inside_repo = True
    except ValueError:
        inside_repo = False

    print("Inside Git repo:", inside_repo)

    if not store.path.exists():
        print("FAIL: database was not created")
        return 1

    if inside_repo:
        print("FAIL: database is inside Git repository")
        return 1

    if record is None or record.response != "HIWAN_SQLITE_OK":
        print("FAIL: persisted record could not be read back")
        return 1

    print("PASS: SQLite persistence works outside Git repository")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
