"""Phase 3-A: Trading Calendar — strict T20/T60 enforcement."""
from __future__ import annotations
import csv
from pathlib import Path
from typing import Optional

class TradingCalendar:
    def __init__(self, csv_path: Optional[str | Path] = None):
        self._open_dates: list[str] = []
        self._date_set: set[str] = set()
        self._next_map: dict[str, str] = {}
        self._prev_map: dict[str, str] = {}
        if csv_path: self._load_csv(Path(csv_path))

    def _load_csv(self, path: Path):
        with open(path, newline="", encoding="utf-8") as f:
            rows = list(csv.DictReader(f))
        open_dates = [r["trade_date"].strip() for r in rows if r.get("is_open","1").strip() in ("1","True","true")]
        self._open_dates = sorted(open_dates)
        self._date_set = set(self._open_dates)
        for i, d in enumerate(self._open_dates):
            if i > 0: self._prev_map[d] = self._open_dates[i-1]
            if i < len(self._open_dates) - 1: self._next_map[d] = self._open_dates[i+1]

    def is_trade_day(self, date: str) -> bool: return date in self._date_set

    def next_trade_day(self, date: str) -> Optional[str]:
        if date in self._next_map: return self._next_map[date]
        for d in self._open_dates:
            if d > date: return d
        return None

    def prev_trade_day(self, date: str) -> Optional[str]:
        if date in self._prev_map: return self._prev_map[date]
        prev = None
        for d in self._open_dates:
            if d >= date: return prev
            prev = d
        return prev

    def forward_trade_day(self, date: str, n: int) -> Optional[str]:
        """Return the date n forward trading days from date. None if insufficient."""
        d = date
        for _ in range(n):
            d = self.next_trade_day(d)
            if d is None: return None
        return d

    def has_forward_days(self, date: str, n: int) -> bool:
        return self.forward_trade_day(date, n) is not None
