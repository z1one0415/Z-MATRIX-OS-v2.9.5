"""PIT Fundamentals Loader — read pre-replay-date financial data only"""
from __future__ import annotations
import csv
from pathlib import Path

def _clean_date(x): return str(x or "").replace("-", "").strip()
def _to_float(x, d=None):
    try: return float(x) if x not in (None, "") else d
    except: return d

def load_pit_fundamental_snapshot(*, ticker, replay_date, local_data_root):
    """Read the latest pre-replay-date financial snapshot from local CSV.

    Searches: data/fundamentals/{ticker}_fin.csv first, then {ticker}.csv
    Handles tushare fina_indicator column names.
    """
    root = Path(local_data_root)
    replay_clean = _clean_date(replay_date)

    candidates = [
        root / "data" / "fundamentals" / f"{ticker}_fin.csv",
        root / "data" / "fundamentals" / f"{ticker}.csv",
    ]

    rows = []
    for path in candidates:
        if not path.exists():
            continue
        with open(path, encoding="utf-8-sig") as f:
            for r in csv.DictReader(f):
                # tushare format: ts_code has the ticker
                ts = r.get("ts_code", "")
                if ts and ts[:6] != str(ticker)[:6]:
                    continue

                # Disclosure date priority: ann_date > end_date > f_ann_date
                d = (_clean_date(r.get("ann_date") or r.get("f_ann_date") or r.get("end_date") or ""))
                if not d:
                    continue

                if d <= replay_clean:
                    rows.append((d, r))
                # Don't break — we want the LATEST row ≤ replay_clean

    if not rows:
        return {
            "snapshot_status": "INSUFFICIENT_DATA",
            "ticker": ticker, "replay_date": replay_date,
            "snapshot": {}, "point_in_time_valid": True,
            "future_data_allowed": False, "real_trade_allowed": False,
        }

    rows.sort(key=lambda x: x[0])
    d, r = rows[-1]

    # Check if we used end_date instead of ann_date (potential PIT weakness)
    has_ann_date = bool(r.get("ann_date") or r.get("f_ann_date"))

    # Map tushare column names to snapshot keys
    s = {
        "disclosure_date": d,
        "report_date": r.get("end_date") or r.get("report_date"),
        "roe": _to_float(r.get("roe")),
        "gross_margin": _to_float(r.get("gross_margin") or r.get("grossprofit_margin")),
        "revenue_yoy": _to_float(r.get("or_yoy") or r.get("revenue_yoy") or r.get("tr_yoy")),
        "profit_yoy": _to_float(r.get("netprofit_yoy") or r.get("profit_yoy") or r.get("dt_netprofit_yoy")),
        "debt_ratio": _to_float(r.get("debt_to_assets") or r.get("debt_ratio")),
        "pe": _to_float(r.get("pe")),
        "pb": _to_float(r.get("pb")),
        "ps": _to_float(r.get("ps")),
        "market_cap": _to_float(r.get("total_mv") or r.get("market_cap")),
        "operating_cashflow": _to_float(r.get("ocfps") or r.get("operating_cashflow")),
    }

    return {
        "snapshot_status": "READY",
        "ticker": ticker, "replay_date": replay_date,
        "snapshot_date": d,
        "snapshot": s,
        "point_in_time_valid": True,
        "potential_pit_weakness": not has_ann_date,
        "future_data_allowed": False,
        "real_trade_allowed": False,
        "broker_order_allowed": False,
    }
