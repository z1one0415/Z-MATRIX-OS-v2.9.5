from __future__ import annotations
from pathlib import Path
from zmatrix.sector_mapping_ingestion.schema import DEFAULT_SECTOR_MAPPING_SAFETY

SEARCH_PATHS = ["data/stock_basic.csv","data/tushare/stock_basic.csv","data/metadata/stock_basic.csv","data/fundamentals/stock_basic.csv","data/industry","data/sector","data/concept","data/metadata"]

def discover_mapping_sources(*, data_root=".") -> dict:
    root = Path(data_root); files = []
    for rel in SEARCH_PATHS:
        p = root/rel
        if p.exists() and p.is_file() and p.suffix.lower() in (".csv",".json"): files.append(str(p))
        elif p.exists() and p.is_dir():
            for f in p.rglob("*"):
                if f.suffix.lower() in (".csv",".json"): files.append(str(f))
    return {"discovery_version":"V3510_MAPPING_SOURCE_DISCOVERY_V10","source_status":"READY" if files else "DATA_INSUFFICIENT","source_count":len(files),"source_files":sorted(files),"real_trade_allowed":False,"broker_order_allowed":False,"safety":dict(DEFAULT_SECTOR_MAPPING_SAFETY)}
