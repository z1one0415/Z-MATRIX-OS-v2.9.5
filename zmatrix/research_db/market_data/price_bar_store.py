"""Phase 3-A: Price Bar Store — load + query + suspension/limit detection."""
from __future__ import annotations
import csv
from pathlib import Path
from typing import Optional

class PriceBarStore:
    def __init__(self, csv_path: Optional[str | Path] = None):
        self._bars: dict[str, dict[str, dict]] = {}
        if csv_path: self._load_csv(Path(csv_path))

    def _load_csv(self, path: Path):
        with open(path, newline="", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                t = row["ticker"].strip()
                d = row["trade_date"].strip()
                self._bars.setdefault(t, {})[d] = {
                    "ticker": t, "trade_date": d,
                    "open": float(row.get("open",0)), "high": float(row.get("high",0)),
                    "low": float(row.get("low",0)), "close": float(row.get("close",0)),
                    "pre_close": float(row.get("pre_close", row.get("open",0))),
                    "volume": int(row.get("volume",0)), "amount": float(row.get("amount",0)),
                    "is_suspended": row.get("is_suspended","0").strip() in ("1","True","true"),
                    "is_limit_up": row.get("is_limit_up","0").strip() in ("1","True","true"),
                    "is_limit_down": row.get("is_limit_down","0").strip() in ("1","True","true"),
                    "is_one_price_limit": row.get("is_one_price_limit","0").strip() in ("1","True","true"),
                }

    def get_bar(self, ticker: str, trade_date: str) -> dict | None:
        return self._bars.get(ticker, {}).get(trade_date)

    def get_bars(self, ticker: str, start_date: str, end_date: str) -> list[dict]:
        ticker_bars = self._bars.get(ticker, {})
        return [b for d, b in sorted(ticker_bars.items()) if start_date <= d <= end_date]

    def has_bar(self, ticker: str, trade_date: str) -> bool:
        return self.get_bar(ticker, trade_date) is not None

    def detect_suspension(self, ticker: str, trade_date: str) -> bool:
        bar = self.get_bar(ticker, trade_date)
        return bar["is_suspended"] if bar else False

    def detect_limit_up(self, ticker: str, trade_date: str) -> bool:
        bar = self.get_bar(ticker, trade_date)
        return bar["is_limit_up"] if bar else False

    def detect_limit_down(self, ticker: str, trade_date: str) -> bool:
        bar = self.get_bar(ticker, trade_date)
        return bar["is_limit_down"] if bar else False

    def detect_one_price_limit(self, ticker: str, trade_date: str) -> bool:
        bar = self.get_bar(ticker, trade_date)
        return bar["is_one_price_limit"] if bar else False
