"""PITStore — Point-in-Time data store with future-access blocking."""
from __future__ import annotations
from dataclasses import dataclass, field
from datetime import date, datetime, timezone


@dataclass
class PITRecord:
    ticker: str
    field_name: str
    value: float
    snapshot_date: str
    recorded_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    production_allowed: bool = field(default=False, repr=False)

    def __post_init__(self):
        self.production_allowed = False


class PITStore:
    def __init__(self):
        self._records: list[PITRecord] = []

    def add_record(self, ticker: str, field_name: str, value: float, snapshot_date: str) -> PITRecord:
        rec = PITRecord(ticker=ticker, field_name=field_name, value=value, snapshot_date=snapshot_date)
        self._records.append(rec)
        return rec

    def query_as_of(self, ticker: str, field_name: str, as_of_date: str) -> list[PITRecord]:
        results = []
        for r in self._records:
            if r.ticker != ticker or r.field_name != field_name:
                continue
            if r.snapshot_date > as_of_date:
                continue
            results.append(r)
        return sorted(results, key=lambda r: r.snapshot_date)

    def get_latest(self, ticker: str, field_name: str, as_of_date: str) -> PITRecord | None:
        candidates = []
        for r in self._records:
            if r.ticker != ticker or r.field_name != field_name:
                continue
            if r.snapshot_date > as_of_date:
                continue
            candidates.append(r)
        if not candidates:
            return None
        return max(candidates, key=lambda r: r.snapshot_date)

    def count(self) -> int:
        return len(self._records)

    def list_all(self) -> list[PITRecord]:
        return list(self._records)
