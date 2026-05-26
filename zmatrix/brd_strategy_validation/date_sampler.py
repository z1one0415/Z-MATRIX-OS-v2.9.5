"""Date Sampler — sample representative replay dates from local price data"""
from __future__ import annotations
import csv
from pathlib import Path

def sample_replay_dates_from_index(*, local_data_root=".", index_code="000001", max_dates=60):
    candidates = [Path(local_data_root)/"data"/"price_bars"/f"{index_code}.csv"]
    rows = []
    for path in candidates:
        if not path.exists(): continue
        with open(path, encoding="utf-8-sig") as f:
            for r in csv.DictReader(f):
                d = (r.get("trade_date") or r.get("date","")).replace("-","")
                if d: rows.append(d)
        if rows: break
    rows = sorted(set(rows))
    if not rows: return {"sample_status":"NO_DATES","dates":[],"real_trade_allowed":False}
    selected = rows if len(rows)<=max_dates else rows[::max(1,len(rows)//max_dates)][:max_dates]
    return {"sample_status":"READY","source_date_count":len(rows),"selected_count":len(selected),
            "dates":selected,"real_trade_allowed":False,"broker_order_allowed":False}
