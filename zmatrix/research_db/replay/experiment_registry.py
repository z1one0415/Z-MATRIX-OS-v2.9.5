"""Batch-C: Experiment Registry — append-only, immutable."""
from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, timezone

@dataclass
class ExperimentRecord:
    experiment_id: str; dataset_id: str; dataset_hash: str
    factor_version: str; parameter_version: str
    start_date: str; end_date: str
    created_time: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    result_hash: str = ""
    production_allowed: bool = field(default=False, repr=False)
    def __post_init__(self): self.production_allowed=False

class ExperimentRegistry:
    def __init__(self): self._records: list[ExperimentRecord] = []
    def register(self, record: ExperimentRecord) -> str:
        self._records.append(record); return record.experiment_id
    def list_all(self) -> list[ExperimentRecord]: return list(self._records)
    def get_by_id(self, experiment_id: str) -> ExperimentRecord | None:
        for r in self._records:
            if r.experiment_id == experiment_id: return r
        return None
    def count(self) -> int: return len(self._records)
    def latest(self, n: int = 5) -> list[ExperimentRecord]:
        return sorted(self._records, key=lambda r: r.created_time, reverse=True)[:n]
