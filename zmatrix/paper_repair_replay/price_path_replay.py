from __future__ import annotations
import csv
from pathlib import Path
from zmatrix.paper_repair_replay.schema import DEFAULT_REPAIR_REPLAY_SAFETY

def _clean_date(x) -> str: return str(x or "").replace("-", "").strip()

def load_price_path_with_dates(*, ticker: str, entry_date: str, data_root: str = ".", max_days: int = 80) -> dict:
    bare = str(ticker).split(".")[0]
    path = Path(data_root) / "data" / "price_bars" / f"{bare}.csv"
    if not path.exists():
        return {"path_status": "MISSING", "ticker": ticker, "bars": [], "safety": dict(DEFAULT_REPAIR_REPLAY_SAFETY), "real_trade_allowed": False, "broker_order_allowed": False}
    entry = _clean_date(entry_date); bars = []
    with open(path, "r", encoding="utf-8-sig") as f:
        for row in csv.DictReader(f):
            d = _clean_date(row.get("trade_date") or row.get("date"))
            if not d or d < entry: continue
            close = row.get("close")
            if close in (None, ""): continue
            try: close_f = float(close)
            except Exception: continue
            bars.append({"trade_date": d, "close": close_f})
            if len(bars) >= max_days: break
    return {"path_status": "READY" if len(bars) >= 5 else "INSUFFICIENT", "ticker": ticker, "entry_date": entry, "bar_count": len(bars), "bars": bars, "safety": dict(DEFAULT_REPAIR_REPLAY_SAFETY), "real_trade_allowed": False, "broker_order_allowed": False}
