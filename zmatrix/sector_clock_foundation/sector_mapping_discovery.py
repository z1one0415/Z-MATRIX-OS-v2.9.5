from __future__ import annotations
import csv
from pathlib import Path
from zmatrix.sector_clock_foundation.schema import DEFAULT_SECTOR_CLOCK_SAFETY

CANDIDATE_FILES = ["data/stock_basic.csv","data/stock_basic.json","data/tushare/stock_basic.csv","data/metadata/stock_basic.csv","data/fundamentals/stock_basic.csv"]
TICKER_FIELDS = ["ts_code","ticker","symbol","code"]
SECTOR_FIELDS = ["industry","sector","sector_code","concept","theme","sw_industry","申万行业","中信行业","同花顺行业"]

def _first(r,fs):
    for f in fs:
        if r.get(f): return r.get(f)
    return None

def discover_sector_mapping(*, data_root=".") -> dict:
    root = Path(data_root); discovered = []; rows = []
    for rel in CANDIDATE_FILES:
        p = root/rel
        if p.exists() and p.suffix.lower()==".csv": discovered.append(str(p)); rows.extend(list(csv.DictReader(open(p,encoding="utf-8-sig"))))
    mapping = {}; fc = {}
    for r in rows:
        t = _first(r, TICKER_FIELDS); s, f = None, None
        for sf in SECTOR_FIELDS:
            if r.get(sf): s = r[sf]; f = sf; break
        if t and s: bare = str(t).split(".")[0]; mapping[bare] = {"ticker":bare,"sector":s,"sector_source_field":f}; fc[f] = fc.get(f,0)+1
    status = "READY" if len(mapping)>=3000 else "PARTIAL" if mapping else "DATA_INSUFFICIENT"
    return {"discovery_version":"V359_SECTOR_MAPPING_DISCOVERY_V10","sector_mapping_status":status,"discovered_files":discovered,"ticker_count":len(mapping),"sector_ready_count":len(mapping),"sector_mapping":mapping,"available_sector_fields":fc,"synthetic_mapping_used":False,"real_trade_allowed":False,"broker_order_allowed":False,"safety":dict(DEFAULT_SECTOR_CLOCK_SAFETY)}
