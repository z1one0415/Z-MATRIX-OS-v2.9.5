# allowlist: forbidden-token-definition
from __future__ import annotations
from pathlib import Path
from zmatrix.sector_clock_foundation.schema import DEFAULT_SECTOR_CLOCK_SAFETY

SEARCH_DIRS = ["data/sector_bars","data/industry_bars","data/sector_index","data/industry_index"]

def discover_sector_indexes(*, data_root=".") -> dict:
    root = Path(data_root); files = []
    for rel in SEARCH_DIRS:
        d = root/rel
        if d.exists() and d.is_dir(): files.extend([str(p) for p in d.glob("*.csv")])
    return {"discovery_version":"V359_SECTOR_INDEX_DISCOVERY_V10","sector_index_status":"READY" if files else "DATA_INSUFFICIENT","sector_index_files":files,"sector_index_count":len(files),"synthetic_sector_index_required":not bool(files),"real_trade_allowed":False,"broker_order_allowed":False,"safety":dict(DEFAULT_SECTOR_CLOCK_SAFETY)}
