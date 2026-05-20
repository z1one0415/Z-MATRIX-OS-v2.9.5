from __future__ import annotations

import json
from dataclasses import dataclass, asdict, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional
from uuid import uuid4


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass(frozen=True)
class EventRecord:
    event_type: str
    payload: Dict[str, Any]
    world: str = "PAPER_WORLD"
    source_ids: List[str] = field(default_factory=list)
    module_versions: Dict[str, str] = field(default_factory=dict)
    llm_assists: bool = False
    event_id: str = field(default_factory=lambda: f"evt_{uuid4().hex[:16]}")
    created_at: str = field(default_factory=now_iso)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class JsonlEventStore:
    """Append-only JSONL event store.

    The store does not support in-place mutation or delete. This is intentional:
    alpha validation records must remain auditable and must not be rewritten by LLMs.
    """

    def __init__(self, path: str | Path):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.touch(exist_ok=True)

    def append(self, record: EventRecord) -> EventRecord:
        if record.world != "PAPER_WORLD":
            raise ValueError("Alpha validation events must be PAPER_WORLD.")
        with self.path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(record.to_dict(), ensure_ascii=False, sort_keys=True) + "\n")
        return record

    def iter_events(self, event_type: Optional[str] = None) -> Iterable[EventRecord]:
        with self.path.open("r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                raw = json.loads(line)
                if event_type and raw.get("event_type") != event_type:
                    continue
                yield EventRecord(**raw)

    def list_events(self, event_type: Optional[str] = None) -> List[EventRecord]:
        return list(self.iter_events(event_type=event_type))

    def by_validation_id(self, validation_id: str) -> List[EventRecord]:
        out: List[EventRecord] = []
        for ev in self.iter_events():
            payload = ev.payload or {}
            if payload.get("validation_id") == validation_id:
                out.append(ev)
        return out
