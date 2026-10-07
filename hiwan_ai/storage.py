from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
import sqlite3


DEFAULT_DEV_DB = Path.home() / ".hiwan" / "dev" / "databases" / "hiwan.db"


@dataclass(frozen=True)
class RunRecord:
    id: int
    created_at: str
    identity: str
    prompt: str
    response: str
    tool_used: str | None
    tool_result: str | None
    status: str


class SQLiteRunStore:
    """Minimal Phase 1 SQLite persistence.

    The default database lives outside the Git repository at:
        ~/.hiwan/dev/databases/hiwan.db
    """

    def __init__(self, path: Path | str = DEFAULT_DEV_DB) -> None:
        self.path = Path(path).expanduser()
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._initialize()

    def _connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self.path)
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA journal_mode=WAL")
        connection.execute("PRAGMA foreign_keys=ON")
        return connection

    def _initialize(self) -> None:
        with self._connect() as connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS agent_runs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    created_at TEXT NOT NULL,
                    identity TEXT NOT NULL,
                    prompt TEXT NOT NULL,
                    response TEXT NOT NULL,
                    tool_used TEXT,
                    tool_result TEXT,
                    status TEXT NOT NULL
                )
                """
            )

    def record_run(
        self,
        *,
        identity: str,
        prompt: str,
        response: str,
        tool_used: str | None = None,
        tool_result: str | None = None,
        status: str = "ok",
    ) -> int:
        created_at = datetime.now(timezone.utc).isoformat()

        with self._connect() as connection:
            cursor = connection.execute(
                """
                INSERT INTO agent_runs (
                    created_at,
                    identity,
                    prompt,
                    response,
                    tool_used,
                    tool_result,
                    status
                )
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    created_at,
                    identity,
                    prompt,
                    response,
                    tool_used,
                    tool_result,
                    status,
                ),
            )
            return int(cursor.lastrowid)

    def get_run(self, run_id: int) -> RunRecord | None:
        with self._connect() as connection:
            row = connection.execute(
                """
                SELECT
                    id,
                    created_at,
                    identity,
                    prompt,
                    response,
                    tool_used,
                    tool_result,
                    status
                FROM agent_runs
                WHERE id = ?
                """,
                (run_id,),
            ).fetchone()

        if row is None:
            return None

        return RunRecord(
            id=int(row["id"]),
            created_at=str(row["created_at"]),
            identity=str(row["identity"]),
            prompt=str(row["prompt"]),
            response=str(row["response"]),
            tool_used=row["tool_used"],
            tool_result=row["tool_result"],
            status=str(row["status"]),
        )

    def count_runs(self) -> int:
        with self._connect() as connection:
            row = connection.execute(
                "SELECT COUNT(*) AS count FROM agent_runs"
            ).fetchone()
        return int(row["count"])
