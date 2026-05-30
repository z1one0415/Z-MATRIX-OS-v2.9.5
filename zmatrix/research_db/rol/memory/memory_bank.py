"""R4: Memory Bank — store historical research objects and results."""
from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, timezone

@dataclass
class MemoryEntry:
    memory_id: str; entry_id: str; object_type: str; content: dict = field(default_factory=dict)
    result: str = ""; stored_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    production_allowed: bool = field(default=False, repr=False)
    def __post_init__(self): self.production_allowed=False

class MemoryBank:
    def __init__(self): self._memories: list[MemoryEntry] = []
    def store(self, memory_id: str, entry_id: str, object_type: str, content: dict = None, result: str = "") -> MemoryEntry:
        m = MemoryEntry(memory_id=memory_id, entry_id=entry_id, object_type=object_type, content=content or {}, result=result)
        self._memories.append(m); return m
    def recall(self, memory_id: str) -> MemoryEntry | None: return next((m for m in self._memories if m.memory_id==memory_id), None)
    def by_entry(self, entry_id: str) -> list[MemoryEntry]: return [m for m in self._memories if m.entry_id==entry_id]
    def by_result(self, result: str) -> list[MemoryEntry]: return [m for m in self._memories if m.result==result]
    def count(self) -> int: return len(self._memories)
