"""Batch-C: Replay Runner — unified replay execution interface."""
from __future__ import annotations
from .replay_dataset import RollingDataset
from dataclasses import dataclass, field
from typing import Optional

@dataclass
class ReplayResult:
    experiment_id: str; status: str = "PENDING"; slices_processed: int = 0
    total_records: int = 0; execution_time_ms: float = 0.0
    replay_hash: str = ""; details: dict = field(default_factory=dict)
    production_allowed: bool = field(default=False, repr=False)
    def __post_init__(self): self.production_allowed=False

class ReplayRunner:
    def __init__(self, dataset, metrics_engine=None, attribution_engine=None):
        self.dataset = dataset; self.metrics = metrics_engine; self.attribution = attribution_engine

    def run_replay(self, experiment_id: str, slices: list, engine_fn=None) -> ReplayResult:
        result = ReplayResult(experiment_id=experiment_id, status="RUNNING")
        for sl in slices:
            if engine_fn: engine_fn(sl)
            result.slices_processed += 1; result.total_records += sl.record_count
        result.status = "COMPLETED"
        return result

    def run_batch_replay(self, experiment_ids: list[str], slices: list) -> list[ReplayResult]:
        return [self.run_replay(eid, slices) for eid in experiment_ids]

    def run_snapshot_replay(self, experiment_id: str, date: str, tickers=None) -> ReplayResult:
        s = self.dataset.slice_by_date(date, date, tickers)
        return self.run_replay(experiment_id, [s])

    def run_rolling_replay(self, experiment_id: str, start: str, end: str, window: int = 20, step: int = 5) -> ReplayResult:
        if self.dataset.cal is None:
            result = ReplayResult(experiment_id=experiment_id, status="FAILED")
            result.details = {"error_type": "CALENDAR_MISSING", "message": "Rolling replay requires a trading calendar"}
            return result
        try:
            ds = RollingDataset(tickers=self.dataset.tickers, bars=self.dataset.bars, cal=self.dataset.cal)
        except ValueError as e:
            result = ReplayResult(experiment_id=experiment_id, status="FAILED")
            result.details = {"error_type": "MALFORMED_TRADING_CALENDAR", "message": str(e)}
            return result
        return self.run_replay(experiment_id, ds.generate_rolling_slices(start, end, window, step))
