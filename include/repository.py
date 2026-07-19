import json
import sqlite3
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterator


class AlertRepository:
    def __init__(self, database_url: str):
        if not database_url.startswith("sqlite:///"):
            raise ValueError("Esta versão suporta DATABASE_URL no formato sqlite:///caminho.db")
        self.database_path = database_url.removeprefix("sqlite:///")
        Path(self.database_path).parent.mkdir(parents=True, exist_ok=True)
        self.initialize()

    @contextmanager
    def connection(self) -> Iterator[sqlite3.Connection]:
        connection = sqlite3.connect(self.database_path)
        connection.row_factory = sqlite3.Row
        try:
            yield connection
            connection.commit()
        finally:
            connection.close()

    def initialize(self) -> None:
        with self.connection() as connection:
            connection.executescript(
                """
                CREATE TABLE IF NOT EXISTS refresh_events (
                    refresh_key TEXT PRIMARY KEY,
                    workspace_id TEXT NOT NULL,
                    workspace_name TEXT NOT NULL,
                    dataset_id TEXT NOT NULL,
                    dataset_name TEXT NOT NULL,
                    status TEXT NOT NULL,
                    start_time TEXT,
                    end_time TEXT,
                    error_code TEXT,
                    error_description TEXT,
                    payload_json TEXT NOT NULL,
                    collected_at TEXT NOT NULL
                );

                CREATE TABLE IF NOT EXISTS incidents (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    refresh_key TEXT NOT NULL UNIQUE,
                    incident_type TEXT NOT NULL,
                    severity TEXT NOT NULL,
                    status TEXT NOT NULL DEFAULT 'open',
                    diagnosis TEXT,
                    opened_at TEXT NOT NULL,
                    resolved_at TEXT,
                    notified_at TEXT,
                    FOREIGN KEY(refresh_key) REFERENCES refresh_events(refresh_key)
                );
                """
            )

    def save_refresh(self, event: dict[str, Any]) -> bool:
        with self.connection() as connection:
            cursor = connection.execute(
                """
                INSERT OR IGNORE INTO refresh_events (
                    refresh_key, workspace_id, workspace_name,
                    dataset_id, dataset_name, status,
                    start_time, end_time, error_code,
                    error_description, payload_json, collected_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    event["refresh_key"],
                    event["workspace_id"],
                    event["workspace_name"],
                    event["dataset_id"],
                    event["dataset_name"],
                    event["status"],
                    event.get("start_time"),
                    event.get("end_time"),
                    event.get("error_code"),
                    event.get("error_description"),
                    json.dumps(event.get("payload", {}), ensure_ascii=False),
                    datetime.now(timezone.utc).isoformat(),
                ),
            )
            return cursor.rowcount == 1

    def create_incident(self, refresh_key: str, diagnosis: str) -> bool:
        with self.connection() as connection:
            cursor = connection.execute(
                """
                INSERT OR IGNORE INTO incidents (
                    refresh_key, incident_type, severity,
                    status, diagnosis, opened_at
                ) VALUES (?, 'REFRESH_FAILED', 'critical', 'open', ?, ?)
                """,
                (refresh_key, diagnosis, datetime.now(timezone.utc).isoformat()),
            )
            return cursor.rowcount == 1

    def mark_notified(self, refresh_key: str) -> None:
        with self.connection() as connection:
            connection.execute(
                "UPDATE incidents SET notified_at = ? WHERE refresh_key = ?",
                (datetime.now(timezone.utc).isoformat(), refresh_key),
            )

    def was_notified(self, refresh_key: str) -> bool:
        with self.connection() as connection:
            row = connection.execute(
                "SELECT notified_at FROM incidents WHERE refresh_key = ?",
                (refresh_key,),
            ).fetchone()
            return bool(row and row["notified_at"])
