from __future__ import annotations
from zmatrix.sector_mapping_ingestion.schema import DEFAULT_SECTOR_MAPPING_SAFETY

def merge_sector_mappings(*, normalized_rows: list[dict]) -> dict:
    merged = {}
    for r in normalized_rows or []:
        tk = r.get("ticker")
        if not tk: continue
        old = merged.get(tk)
        if old is None or _score(r) > _score(old): merged[tk] = r
    ready = {k:v for k,v in merged.items() if v.get("sector") not in (None,"")}
    return {"merger_version":"V3510_MAPPING_MERGER_V10","merged_count":len(merged),"sector_ready_count":len(ready),"sector_mapping":merged,"real_trade_allowed":False,"broker_order_allowed":False,"safety":dict(DEFAULT_SECTOR_MAPPING_SAFETY)}

def _score(r):
    sf = str(r.get("source_field","") or r.get("source_file","")).lower(); s=0
    if r.get("sector"): s+=10
    if "申万" in sf or "sw" in sf: s+=10
    if "中信" in sf: s+=8
    if "industry" in sf: s+=6
    if r.get("theme"): s+=2
    if r.get("market"): s+=1
    return s
