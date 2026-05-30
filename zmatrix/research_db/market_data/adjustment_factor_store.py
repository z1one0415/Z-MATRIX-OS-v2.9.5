"""Phase 3-A: Adjustment Factor Store."""
from __future__ import annotations
import csv
from pathlib import Path
from typing import Optional

class AdjustmentFactorStore:
    def __init__(self, csv_path: Optional[str | Path] = None):
        self._factors: dict[str, dict[str, float]] = {}
        if csv_path: self._load_csv(Path(csv_path))

    def _load_csv(self, path: Path):
        with open(path, newline="", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                t = row["ticker"].strip(); d = row["trade_date"].strip()
                self._factors.setdefault(t, {})[d] = float(row.get("adj_factor", 1.0))

    def get_factor(self, ticker: str, trade_date: str) -> float:
        return self._factors.get(ticker, {}).get(trade_date, 1.0)
