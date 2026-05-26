"""Local SQLite EventStore — append-only, idempotent, conflict-safe

- append-only writes
- Same event_id + same payload → idempotent
- Same event_id + different payload → conflict (no overwrite)
- No real Z9 write
- No Hermes memory write
"""
from __future__ import annotations
import json
import sqlite3
from pathlib import Path
from typing import Any

from zmatrix.event_store.validators import validate_event

_DEFAULT_DB_PATH = "data/event_store/event_store.sqlite"


class LocalEventStore:
    """Append-only local SQLite EventStore."""

    def __init__(self, db_path: str | None = None):
        self._db_path = db_path or _DEFAULT_DB_PATH
        self._conn: sqlite3.Connection | None = None

    def initialize(self) -> None:
        """Create the SQLite table if not exists."""
        Path(self._db_path).parent.mkdir(parents=True, exist_ok=True)
        self._conn = sqlite3.connect(self._db_path)
        self._conn.execute("""
            CREATE TABLE IF NOT EXISTS events (
                event_id TEXT PRIMARY KEY,
                event_type TEXT NOT NULL,
                schema_version TEXT NOT NULL,
                created_at TEXT NOT NULL,
                producer_module TEXT NOT NULL,
                source_event_id TEXT,
                parent_event_id TEXT,
                input_hash TEXT,
                output_hash TEXT,
                payload_json TEXT NOT NULL,
                safety_json TEXT NOT NULL
            )
        """)
        self._conn.commit()

    def _get_connection(self) -> sqlite3.Connection:
        if self._conn is None:
            self.initialize()
        assert self._conn is not None
        return self._conn

    def append_event(self, event: dict) -> dict[str, Any]:
        """Append one event.

        Returns:
            {"event_id": ..., "stored": bool, "idempotent": bool, "conflict": bool,
             "real_z9_write_allowed": False, "hermes_memory_write_allowed": False}
        """
        violations = validate_event(event)
        if violations:
            return {
                "event_id": event.get("event_id", ""),
                "stored": False,
                "idempotent": False,
                "conflict": False,
                "errors": violations,
                "real_z9_write_allowed": False,
                "hermes_memory_write_allowed": False,
            }

        eid = event["event_id"]
        conn = self._get_connection()

        existing = conn.execute(
            "SELECT payload_json FROM events WHERE event_id = ?", (eid,)
        ).fetchone()

        if existing is not None:
            existing_payload = existing[0]
            new_payload = json.dumps(event.get("payload", {}), sort_keys=True)
            if existing_payload == new_payload:
                return {
                    "event_id": eid,
                    "stored": True,
                    "idempotent": True,
                    "conflict": False,
                    "real_z9_write_allowed": False,
                    "hermes_memory_write_allowed": False,
                }
            else:
                return {
                    "event_id": eid,
                    "stored": False,
                    "idempotent": False,
                    "conflict": True,
                    "real_z9_write_allowed": False,
                    "hermes_memory_write_allowed": False,
                }

        conn.execute(
            """INSERT INTO events
               (event_id, event_type, schema_version, created_at, producer_module,
                source_event_id, parent_event_id, input_hash, output_hash,
                payload_json, safety_json)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                eid,
                event["event_type"],
                event.get("schema_version", ""),
                event["created_at"],
                event["producer_module"],
                event.get("source_event_id"),
                event.get("parent_event_id"),
                event.get("input_hash"),
                event.get("output_hash"),
                json.dumps(event.get("payload", {}), sort_keys=True),
                json.dumps(event.get("safety", {}), sort_keys=True),
            ),
        )
        conn.commit()

        return {
            "event_id": eid,
            "stored": True,
            "idempotent": False,
            "conflict": False,
            "real_z9_write_allowed": False,
            "hermes_memory_write_allowed": False,
        }

    def get_event(self, event_id: str) -> dict | None:
        """Retrieve a single event by event_id."""
        conn = self._get_connection()
        row = conn.execute(
            "SELECT * FROM events WHERE event_id = ?", (event_id,)
        ).fetchone()
        if row is None:
            return None
        return self._row_to_dict(row)

    def list_events(self, event_type: str | None = None) -> list[dict]:
        """List all events, optionally filtered by event_type."""
        conn = self._get_connection()
        if event_type:
            rows = conn.execute(
                "SELECT * FROM events WHERE event_type = ? ORDER BY created_at",
                (event_type,),
            ).fetchall()
        else:
            rows = conn.execute(
                "SELECT * FROM events ORDER BY created_at"
            ).fetchall()
        return [self._row_to_dict(r) for r in rows]

    def close(self) -> None:
        if self._conn:
            self._conn.close()
            self._conn = None

    @staticmethod
    def _row_to_dict(row: sqlite3.Row) -> dict:
        return {
            "event_id": row[0],
            "event_type": row[1],
            "schema_version": row[2],
            "created_at": row[3],
            "producer_module": row[4],
            "source_event_id": row[5],
            "parent_event_id": row[6],
            "input_hash": row[7],
            "output_hash": row[8],
            "payload": json.loads(row[9]),
            "safety": json.loads(row[10]),
        }
