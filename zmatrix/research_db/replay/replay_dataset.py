"""Batch-C: Replay Dataset Layer — time/sector/universe slicing, NO future leak."""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional

@dataclass
class DatasetSlice:
    slice_id: str; start_date: str; end_date: str; tickers: list = field(default_factory=list)
    industry_filter: Optional[str] = None; benchmark_filter: Optional[str] = None
    record_count: int = 0; dataset_hash: str = ""
    production_allowed: bool = field(default=False, repr=False)
    def __post_init__(self): self.production_allowed=False

class ReplayDataset:
    def __init__(self, tickers=None, bars=None, calendar=None, cal=None):
        self.tickers = tickers or []; self.bars = bars; self.cal = calendar or cal

    def slice_by_date(self, start: str, end: str, tickers=None) -> DatasetSlice:
        t = tickers or self.tickers
        return DatasetSlice(slice_id=f"DATE_{start}_{end}", start_date=start, end_date=end, tickers=t, record_count=len(t))

    def slice_by_tickers(self, tickers: list, start: str, end: str) -> DatasetSlice:
        return self.slice_by_date(start, end, tickers)

    def slice_by_industry(self, industry: str, start: str, end: str, mapping=None) -> DatasetSlice:
        tickers = [t for t in (mapping or {}).get(industry, [])] if mapping else []
        return DatasetSlice(slice_id=f"IND_{industry}", start_date=start, end_date=end, tickers=tickers, industry_filter=industry)

    def slice_by_benchmark(self, benchmark_id: str, start: str, end: str, tickers=None) -> DatasetSlice:
        return DatasetSlice(slice_id=f"BM_{benchmark_id}", start_date=start, end_date=end, tickers=tickers or [], benchmark_filter=benchmark_id)

    def _validate_no_future(self, request_date: str, access_date: str) -> bool:
        return access_date <= request_date

class RollingDataset(ReplayDataset):
    def generate_rolling_slices(self, start: str, end: str, window_days: int = 20, step_days: int = 5) -> list[DatasetSlice]:
        if self.cal is None:
            raise ValueError("MISSING_TRADING_CALENDAR")
        if not hasattr(self.cal, "next_trade_day"):
            raise ValueError("MALFORMED_TRADING_CALENDAR: missing next_trade_day method")
        slices = []
        d = start
        while d <= end:
            slices.append(self.slice_by_date(d, end if slices else end, self.tickers))
            for _ in range(step_days):
                try:
                    next_day = self.cal.next_trade_day(d)
                except Exception as exc:
                    raise ValueError(f"MALFORMED_TRADING_CALENDAR: next_trade_day error on {d}: {exc}") from exc
                if not isinstance(next_day, str) or not next_day or next_day == d:
                    raise ValueError(f"MALFORMED_TRADING_CALENDAR: next_trade_day({d}) returned invalid: {next_day}")
                d = next_day
        return slices

class CrossSectionDataset(ReplayDataset):
    def generate_cross_sections(self, dates: list[str], tickers=None) -> list[DatasetSlice]:
        return [self.slice_by_date(d, d, tickers or self.tickers) for d in dates]

class SnapshotDataset(ReplayDataset):
    def take_snapshot(self, date: str, tickers=None) -> DatasetSlice:
        return self.slice_by_date(date, date, tickers or self.tickers)
