"""Forward Price Loader — load T+N prices from CSV for outcome backfill only"""
from __future__ import annotations
import csv
from pathlib import Path

def load_forward_price_path(*, ticker, entry_date, local_data_root, max_horizon=60, price_field="close"):
    bare = ticker.split(".")[0]  # strip .SZ/.SH/.BJ suffix
    path = Path(local_data_root) / "data" / "price_bars" / f"{bare}.csv"
    if not path.exists(): return {"ticker":ticker,"entry_date":entry_date,"price_path":[],"status":"MISSING_FILE","real_trade_allowed":False}
    entry_clean = entry_date.replace("-","")
    valid = []
    for r in csv.DictReader(open(path,encoding="utf-8-sig")):
        d = (r.get("trade_date") or r.get("date","")).replace("-","")
        if d > entry_clean:
            try: px = float(r.get(price_field,0)or 0)
            except: continue
            if px > 0: valid.append(float(px))
    selected = valid[:max_horizon]
    return {"ticker":ticker,"entry_date":entry_date,"price_path":selected,
            "available_days":len(selected),
            "status":"READY" if len(selected)>=min(5,max_horizon) else "INSUFFICIENT_FORWARD_DATA",
            "future_feature_leak_allowed":False,"real_trade_allowed":False}
