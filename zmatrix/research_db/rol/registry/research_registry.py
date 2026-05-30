"""R1: Research Registry — unified registration of all research objects."""
from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime, timezone

class ResearchObjectType(str, Enum): THESIS="THESIS"; FACTOR="FACTOR"; PORTFOLIO="PORTFOLIO"; PREDICTION="PREDICTION"; COUNCIL="COUNCIL"

@dataclass
class RegistryEntry:
    entry_id: str; object_type: str; ticker: str = ""; name: str = ""; state: str = "ACTIVE"
    registered_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat()); tags: list = field(default_factory=list)
    production_allowed: bool = field(default=False, repr=False)
    def __post_init__(self): self.production_allowed=False

class ResearchRegistry:
    def __init__(self): self._entries: list[RegistryEntry] = []
    def register(self, entry_id: str, object_type: str, ticker: str = "", name: str = "", tags: list = None) -> RegistryEntry:
        e = RegistryEntry(entry_id=entry_id, object_type=object_type, ticker=ticker, name=name, tags=tags or []); self._entries.append(e); return e
    def get(self, entry_id: str) -> RegistryEntry | None: return next((e for e in self._entries if e.entry_id==entry_id), None)
    def by_type(self, object_type: str) -> list[RegistryEntry]: return [e for e in self._entries if e.object_type==object_type]
    def list_all(self) -> list[RegistryEntry]: return list(self._entries)
    def count(self) -> int: return len(self._entries)
