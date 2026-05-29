# allowlist: forbidden-token-definition
from __future__ import annotations
import csv
from pathlib import Path
from collections import Counter
from zmatrix.synthetic_sector_index.schema import DEFAULT_SYNTHETIC_SECTOR_SAFETY

def load_sector_mapping(*, mapping_path="data/metadata/sector_mapping_v3510.csv") -> dict:
    p = Path(mapping_path)
    if not p.exists(): return {"load_status":"DATA_INSUFFICIENT","sector_mapping":{},"safety":dict(DEFAULT_SYNTHETIC_SECTOR_SAFETY),"real_trade_allowed":False,"broker_order_allowed":False}
    mapping = {}; sc = Counter()
    with open(p,"r",encoding="utf-8-sig") as f:
        for r in csv.DictReader(f):
            tk = str(r.get("ticker","")).split(".")[0].zfill(6); s = r.get("sector") or r.get("industry") or r.get("sector_code")
            if tk and s: mapping[tk]={"ticker":tk,"sector":s,"industry":s}; sc[s]+=1
    return {"loader_version":"V3511_SECTOR_MAPPING_LOADER_V10","load_status":"READY" if mapping else "DATA_INSUFFICIENT","ticker_count":len(mapping),"sector_count":len(sc),"sector_counts":dict(sc),"sector_mapping":mapping,"real_trade_allowed":False,"broker_order_allowed":False,"safety":dict(DEFAULT_SYNTHETIC_SECTOR_SAFETY)}
