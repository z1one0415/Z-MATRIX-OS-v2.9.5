"""Price Path — read local price bars for a ticker from a given start date"""
from __future__ import annotations
from pathlib import Path

def get_price_path(ticker: str, entry_date: str, data_root: str, max_days: int = 80) -> list[float] | None:
    """Read close prices from data/price_bars/{ticker}.csv starting from entry_date.
    Returns list[float] of close prices, or None if unavailable or insufficient data.
    """
    path = Path(data_root) / "data" / "price_bars" / f"{ticker}.csv"
    if not path.exists():
        return None
    try:
        import csv
        closes = []
        found_entry = False
        with open(path, "r", encoding="utf-8-sig") as f:
            for row in csv.DictReader(f):
                date_val = row.get("trade_date") or row.get("date", "")
                close_val = row.get("close")
                if date_val >= entry_date:
                    found_entry = True
                if found_entry and close_val:
                    closes.append(float(close_val))
                    if len(closes) >= max_days:
                        break
        return closes if len(closes) >= 5 else None
    except Exception:
        return None
