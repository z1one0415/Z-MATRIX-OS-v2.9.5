# allowlist: forbidden-token-definition
"""PIT Fundamentals Loader — supports tushare fina_indicator + old B-Matrix format"""
from __future__ import annotations
import csv
from pathlib import Path

def _clean_date(x): return str(x or "").replace("-","").strip()
def _to_float(x, d=None):
    try: return float(x) if x not in (None,"") else d
    except: return d

def _no_data(ticker, replay_date):
    return {"snapshot_status":"INSUFFICIENT_DATA","ticker":ticker,"replay_date":replay_date,
            "snapshot":{},"point_in_time_valid":True,"future_data_allowed":False,"real_trade_allowed":False}

def _parse_tushare_row(d, r, replay_clean):
    """Parse tushare fina_indicator row."""
    gm = _to_float(r.get("grossprofit_margin"))
    if gm is None:
        gm_raw = _to_float(r.get("gross_margin"))
        if gm_raw is not None and gm_raw < 200: gm = gm_raw
    return {
        "disclosure_date": d,
        "report_date": r.get("end_date",""),
        "roe": _to_float(r.get("roe_yearly")) or _to_float(r.get("roe")),
        "gross_margin": gm,
        "revenue_yoy": _to_float(r.get("or_yoy") or r.get("revenue_yoy") or r.get("tr_yoy")),
        "profit_yoy": _to_float(r.get("netprofit_yoy") or r.get("profit_yoy") or r.get("dt_netprofit_yoy")),
        "debt_ratio": _to_float(r.get("debt_to_assets")),
        "pe": _to_float(r.get("pe")),
        "pb": _to_float(r.get("pb")),
        "eps": _to_float(r.get("eps") or r.get("diluted2_eps")),
        "bps": _to_float(r.get("bps")),
        "ps": _to_float(r.get("ps")),
        "market_cap": _to_float(r.get("total_mv")),
        "operating_cashflow": _to_float(r.get("ocfps")),
    }

def _parse_old_format_row(r):
    """Parse old-format _fin.csv (from ingest_core_universe.py).
    Columns: symbol, has_finance, roe_5y_avg, gross_margin(abs), debt_ratio(decimal), pe_ttm, pb
    Advantage: HAS PE/PB!
    """
    if r.get("has_finance") not in (True, "True", 1, "1"):
        return None
    # roe_5y_avg is decimal (0.028 → 2.8%)
    roe_val = _to_float(r.get("roe_5y_avg"))
    roe_pct = round(roe_val * 100, 2) if roe_val is not None else None
    # gross_margin is absolute yuan → skip unless small enough to be percentage
    gm_raw = _to_float(r.get("gross_margin"))
    gm_pct = gm_raw if (gm_raw is not None and gm_raw < 200) else None
    # debt_ratio might be decimal (0.43 → 43%) or already pct (43)
    dr_raw = _to_float(r.get("debt_ratio"))
    dr_pct = round(dr_raw * 100, 2) if (dr_raw is not None and dr_raw < 10) else dr_raw
    return {
        "disclosure_date": _clean_date(r.get("created_at") or r.get("end_date")),
        "report_date": r.get("end_date",""),
        "roe": roe_pct,
        "gross_margin": gm_pct,
        "revenue_yoy": None,
        "profit_yoy": None,
        "debt_ratio": dr_pct,
        "pe": _to_float(r.get("pe_ttm")),
        "pb": _to_float(r.get("pb")),
        "eps": _to_float(r.get("eps") or r.get("diluted2_eps")),
        "bps": _to_float(r.get("bps")),
        "ps": None,
        "market_cap": None,
        "operating_cashflow": None,
    }


def load_pit_fundamental_snapshot(*, ticker, replay_date, local_data_root):
    """Read the latest pre-replay-date financial snapshot from local CSV.
    Supports:
      1. data/fundamentals/{ticker}_fin.csv (tushare fina_indicator)
      2. data/fundamentals/{ticker}_fin.csv (old B-Matrix format)
      3. data/fundamentals/{ticker}.csv (fallback)
    """
    root = Path(local_data_root)
    replay_clean = _clean_date(replay_date)

    paths = [
        root / "data" / "fundamentals" / f"{ticker}_fin.csv",
        root / "data" / "fundamentals" / f"{ticker}.csv",
    ]

    for path in paths:
        if not path.exists():
            continue
        with open(path, encoding="utf-8-sig") as f:
            rows = list(csv.DictReader(f))
        if not rows:
            continue

        cols = set(rows[0].keys())
        is_old_format = "symbol" in cols and "has_finance" in cols and "ts_code" not in cols

        if is_old_format:
            # Single-row old format
            r = rows[0]
            snap = _parse_old_format_row(r)
            if snap is None:
                return _no_data(ticker, replay_date)
            return {"snapshot_status":"READY","ticker":ticker,"replay_date":replay_date,
                    "snapshot_date": snap["disclosure_date"],"snapshot":snap,
                    "point_in_time_valid":True,"potential_pit_weakness":True,
                    "future_data_allowed":False,"real_trade_allowed":False,"broker_order_allowed":False}

        # Tushare format: filter by ann_date ≤ replay_date
        data_rows = []
        for r in rows:
            ts = r.get("ts_code","")
            if ts and ts[:6] != str(ticker)[:6]:
                continue
            d = _clean_date(r.get("ann_date") or r.get("f_ann_date") or r.get("end_date") or "")
            if not d: continue
            if d <= replay_clean:
                data_rows.append((d, r))

        if not data_rows:
            continue  # try next file

        data_rows.sort(key=lambda x: x[0])
        d, r = data_rows[-1]
        has_ann = bool(r.get("ann_date") or r.get("f_ann_date"))
        snap = _parse_tushare_row(d, r, replay_clean)
        return {"snapshot_status":"READY","ticker":ticker,"replay_date":replay_date,
                "snapshot_date":d,"snapshot":snap,
                "point_in_time_valid":True,"potential_pit_weakness":not has_ann,
                "future_data_allowed":False,"real_trade_allowed":False,"broker_order_allowed":False}

    return _no_data(ticker, replay_date)
