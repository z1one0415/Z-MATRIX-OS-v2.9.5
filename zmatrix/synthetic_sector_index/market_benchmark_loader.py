from __future__ import annotations
import csv
from pathlib import Path
from zmatrix.synthetic_sector_index.schema import DEFAULT_SYNTHETIC_SECTOR_SAFETY

INDEX_PRIORITY = ["000001","000905","000852","000300"]

def _tf(x):
    try:
        if x in (None,""): return None
        return float(x)
    except: return None

def load_market_benchmark(*, data_root=".") -> dict:
    for code in INDEX_PRIORITY:
        for d in ["data/index_bars","data/price_bars"]:
            p = Path(data_root)/d/f"{code}.csv"
            if not p.exists(): continue
            rows = []
            with open(p,"r",encoding="utf-8-sig") as f:
                for r in csv.DictReader(f):
                    dt = str(r.get("trade_date") or r.get("date","")).replace("-","")[:8]; c = _tf(r.get("close"))
                    if dt and c is not None: rows.append({"trade_date":dt,"close":c})
            if rows: return {"benchmark_status":"READY","benchmark_code":code,"bars":sorted(rows,key=lambda x:x["trade_date"]),"real_trade_allowed":False,"broker_order_allowed":False,"safety":dict(DEFAULT_SYNTHETIC_SECTOR_SAFETY)}
    return {"benchmark_status":"DATA_INSUFFICIENT","benchmark_code":None,"bars":[],"real_trade_allowed":False,"broker_order_allowed":False,"safety":dict(DEFAULT_SYNTHETIC_SECTOR_SAFETY)}
