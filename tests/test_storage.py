from pathlib import Path

from hiwan_ai.storage import SQLiteRunStore


def test_sqlite_run_store_round_trip(tmp_path: Path) -> None:
    db_path = tmp_path / "test.db"
    store = SQLiteRunStore(db_path)

    run_id = store.record_run(
        identity="richard",
        prompt="hello",
        response="world",
        tool_used="test_tool",
        tool_result="result",
        status="ok",
    )

    record = store.get_run(run_id)

    assert record is not None
    assert record.id == run_id
    assert record.identity == "richard"
    assert record.prompt == "hello"
    assert record.response == "world"
    assert record.tool_used == "test_tool"
    assert record.tool_result == "result"
    assert record.status == "ok"
    assert store.count_runs() == 1


def test_sqlite_store_creates_parent_directories(tmp_path: Path) -> None:
    db_path = tmp_path / "nested" / "databases" / "test.db"

    SQLiteRunStore(db_path)

    assert db_path.exists()
