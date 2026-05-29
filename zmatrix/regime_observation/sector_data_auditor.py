# allowlist: forbidden-token-definition
from __future__ import annotations
from zmatrix.regime_observation.schema import DEFAULT_REGIME_OBSERVATION_SAFETY

def _extract_sector(row):
    if row.get("sector"): return row["sector"],"sector"
    if row.get("industry"): return row["industry"],"industry"
    brd = (row.get("source_brd_result") or {})
    if brd.get("sector"): return brd["sector"],"source_brd_result.sector"
    if brd.get("industry"): return brd["industry"],"source_brd_result.industry"
    raw = brd.get("source_raw") or {}; raw2 = row.get("source_raw") or {}
    if raw.get("sector") or raw2.get("sector"): return raw.get("sector") or raw2.get("sector"),"source_raw.sector"
    if raw.get("industry") or raw2.get("industry"): return raw.get("industry") or raw2.get("industry"),"source_raw.industry"
    return None,None

def audit_sector_data(*, rows: list[dict]) -> dict:
    t=len(rows or []); r=0; fc={}
    for row in rows or []:
        sec,f = _extract_sector(row)
        if sec: r+=1; fc[f]=fc.get(f,0)+1
    cov = r/t if t else 0
    status = "SECTOR_DATA_READY" if cov>=0.70 else "SECTOR_DATA_PARTIAL" if cov>0 else "SECTOR_DATA_INSUFFICIENT"
    return {"auditor_version":"V358_SECTOR_DATA_AUDIT_V10","sector_data_status":status,"total_rows":t,"sector_ready_count":r,"sector_missing_count":t-r,"sector_field_coverage":cov,"available_sector_fields":fc,"real_trade_allowed":False,"broker_order_allowed":False,"safety":dict(DEFAULT_REGIME_OBSERVATION_SAFETY)}

def profile_sector_exposure(*, rows: list[dict]) -> dict:
    from collections import Counter
    sectors = []
    for r in rows or []:
        sec,_ = _extract_sector(r)
        if sec: sectors.append(sec)
    if not sectors: return {"profile_version":"V358_SECTOR_EXPOSURE_PROFILE_V10","sector_profile_status":"DATA_INSUFFICIENT","sector_counts":{},"top_sectors":[],"real_trade_allowed":False,"broker_order_allowed":False,"safety":dict(DEFAULT_REGIME_OBSERVATION_SAFETY)}
    c=Counter(sectors); total=len(sectors)
    return {"profile_version":"V358_SECTOR_EXPOSURE_PROFILE_V10","sector_profile_status":"READY","sector_counts":dict(c),"top_sectors":c.most_common(20),"top_sector_share":c.most_common(1)[0][1]/total if total else None,"real_trade_allowed":False,"broker_order_allowed":False,"safety":dict(DEFAULT_REGIME_OBSERVATION_SAFETY)}
