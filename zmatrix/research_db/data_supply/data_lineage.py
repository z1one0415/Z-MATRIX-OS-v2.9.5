"""DataLineage — trace factor computation provenance from source through transforms."""
from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, timezone


@dataclass
class LineageEntry:
    factor_id: str
    source: str
    transform: str
    input_fields: list[str] = field(default_factory=list)
    output_field: str = ""
    upstream_factor_ids: list[str] = field(default_factory=list)
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    production_allowed: bool = field(default=False, repr=False)

    def __post_init__(self):
        self.production_allowed = False


class DataLineage:
    def __init__(self):
        self._entries: dict[str, LineageEntry] = {}
        self._graph: dict[str, list[str]] = {}

    def add_entry(self, entry: LineageEntry) -> str:
        self._entries[entry.factor_id] = entry
        for upstream in entry.upstream_factor_ids:
            if upstream not in self._graph:
                self._graph[upstream] = []
            self._graph[upstream].append(entry.factor_id)
        return entry.factor_id

    def trace(self, factor_id: str) -> list[LineageEntry]:
        if factor_id not in self._entries:
            return []
        visited: set[str] = set()
        result: list[LineageEntry] = []

        def _dfs(fid: str):
            if fid in visited:
                return
            visited.add(fid)
            if fid in self._entries:
                entry = self._entries[fid]
                result.append(entry)
                for upstream in entry.upstream_factor_ids:
                    _dfs(upstream)

        _dfs(factor_id)
        return result

    def get_entry(self, factor_id: str) -> LineageEntry | None:
        return self._entries.get(factor_id)

    def count(self) -> int:
        return len(self._entries)

    def list_all(self) -> list[LineageEntry]:
        return list(self._entries.values())

    def downstream(self, factor_id: str) -> list[str]:
        return list(self._graph.get(factor_id, []))
