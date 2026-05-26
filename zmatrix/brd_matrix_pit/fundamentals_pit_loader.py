"""PIT Fundamentals Loader — read pre-replay-date financial data only"""
from __future__ import annotations
import csv
from pathlib import Path

def _clean_date(x): return str(x or "").replace("-","").strip()
def _to_float(x, d=None):
    try: return float(x) if x not in (None,"") else d
    except: return d

def load_pit_fundamental_snapshot(*, ticker, replay_date, local_data_root):
    root = Path(local_data_root); replay_clean = _clean_date(replay_date)
    paths = [root/"data"/"fundamentals"/f"{ticker}.csv", root/"data"/"fundamentals.csv"]
    rows = []
    for path in paths:
        if not path.exists(): continue
        with open(path, encoding="utf-8-sig") as f:
            for r in csv.DictReader(f):
                code = str(r.get("ticker") or r.get("ts_code") or r.get("symbol") or ticker)
                if code.replace(".SZ","").replace(".SH","")[:6] != str(ticker)[:6]: continue
                d = _clean_date(r.get("ann_date") or r.get("disclosure_date") or r.get("publish_date") or r.get("report_date") or r.get("end_date") or "")
                if not d: continue
                if d <= replay_clean: rows.append((d, r))
    if not rows:
        return {"snapshot_status":"INSUFFICIENT_DATA","ticker":ticker,"replay_date":replay_date,
                "snapshot":{},"point_in_time_valid":True,"future_data_allowed":False,"real_trade_allowed":False}
    rows.sort(key=lambda x:x[0]); d, r = rows[-1]
    s = {"disclosure_date":d, "roe":_to_float(r.get("roe")), "gross_margin":_to_float(r.get("gross_margin")),
         "revenue_yoy":_to_float(r.get("revenue_yoy")), "profit_yoy":_to_float(r.get("profit_yoy")),
         "debt_ratio":_to_float(r.get("debt_ratio")), "pe":_to_float(r.get("pe")), "pb":_to_float(r.get("pb"))}
    return {"snapshot_status":"READY","ticker":ticker,"replay_date":replay_date,"snapshot_date":d,"snapshot":s,
            "point_in_time_valid":True,"future_data_allowed":False,"real_trade_allowed":False,"broker_order_allowed":False}
