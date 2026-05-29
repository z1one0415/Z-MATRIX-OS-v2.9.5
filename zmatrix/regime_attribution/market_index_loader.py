# allowlist: forbidden-token-definition
from __future__ import annotations
import csv
from pathlib import Path
from zmatrix.regime_attribution.schema import DEFAULT_REGIME_ATTRIBUTION_SAFETY

INDEX_PRIORITY = ["000001","000300","000905","000852"]
INDEX_DIRS = ["data/index_bars","data/price_bars"]

def _clean(x): return str(x or "").replace("-","").strip()
def _to_float(x):
    try:
        if x in (None,""): return None
        return float(x)
    except: return None

def load_index_data(*, data_root: str = ".") -> dict:
    available = {}; missing = []
    for code in INDEX_PRIORITY:
        found = False
        for d in INDEX_DIRS:
            p = Path(data_root)/d/f"{code}.csv"
            if p.exists():
                bars = {}
                with open(p,"r",encoding="utf-8-sig") as f:
                    for row in csv.DictReader(f):
                        dt = _clean(row.get("trade_date") or row.get("date"))
                        close = _to_float(row.get("close"))
                        vol = _to_float(row.get("vol") or row.get("volume"))
                        if not dt or close is None: continue
                        bars[dt] = {"close":close,"volume":vol}
                available[code] = {"bar_count":len(bars),"bars":bars}
                found = True; break
        if not found: missing.append(code)
    status = "READY" if available else "DATA_INSUFFICIENT"
    return {"index_data_version":"V356_INDEX_DATA_V10","index_data_status":status,"available_indexes":list(available.keys()),"missing_indexes":missing,"index_data":available,"needs_network_fetch":False,"real_trade_allowed":False,"broker_order_allowed":False,"safety":dict(DEFAULT_REGIME_ATTRIBUTION_SAFETY)}
