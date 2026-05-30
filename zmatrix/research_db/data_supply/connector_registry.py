"""ConnectorRegistry — source connector registration and lookup."""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional

SUPPORTED_SOURCES = ["akshare", "tushare", "baostock", "yahoo", "fred", "stooq"]


@dataclass
class ConnectorEntry:
    source: str
    module_path: str
    class_name: str
    enabled: bool = True
    priority: int = 0
    metadata: dict = field(default_factory=dict)
    production_allowed: bool = field(default=False, repr=False)

    def __post_init__(self):
        self.production_allowed = False
        if self.source not in SUPPORTED_SOURCES:
            raise ValueError(f"Unsupported source: {self.source}. Must be one of {SUPPORTED_SOURCES}")


class ConnectorRegistry:
    def __init__(self):
        self._entries: dict[str, list[ConnectorEntry]] = {s: [] for s in SUPPORTED_SOURCES}

    def register(self, entry: ConnectorEntry) -> str:
        if entry.source not in self._entries:
            raise ValueError(f"Unsupported source: {entry.source}")
        self._entries[entry.source].append(entry)
        return f"{entry.source}:{entry.class_name}"

    def get(self, source: str, class_name: str | None = None) -> ConnectorEntry | list[ConnectorEntry] | None:
        if source not in self._entries:
            return None
        entries = self._entries[source]
        if class_name is None:
            return list(entries)
        for e in entries:
            if e.class_name == class_name:
                return e
        return None

    def list_all(self) -> list[ConnectorEntry]:
        result = []
        for entries in self._entries.values():
            result.extend(entries)
        return sorted(result, key=lambda e: (-e.priority, e.source))

    def count(self, source: str | None = None) -> int:
        if source is not None:
            if source not in self._entries:
                return 0
            return len(self._entries[source])
        return sum(len(v) for v in self._entries.values())

    def list_sources(self) -> list[str]:
        return list(SUPPORTED_SOURCES)
