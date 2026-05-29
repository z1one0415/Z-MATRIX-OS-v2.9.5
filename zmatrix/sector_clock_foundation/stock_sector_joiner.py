# allowlist: forbidden-token-definition
from __future__ import annotations
from zmatrix.sector_clock_foundation.schema import DEFAULT_SECTOR_CLOCK_SAFETY

def join_stock_sector_mapping(*, rows: list[dict], sector_mapping: dict) -> dict:
    joined = []; ready = 0
    for row in rows or []:
        ticker = str(row.get("ticker") or "").split(".")[0]; meta = sector_mapping.get(ticker,{})
        r2 = dict(row)
        if meta: r2["sector"]=meta.get("sector"); r2["sector_source_field"]=meta.get("sector_source_field"); r2["sector_join_status"]="READY"; ready+=1
        else: r2["sector_join_status"]="MISSING"
        r2["uses_future_data"]=False; joined.append(r2)
    total = len(rows or []); cov = ready/total if total else 0
    return {"join_version":"V359_STOCK_SECTOR_JOIN_V10","total_rows":total,"sector_join_ready_count":ready,"sector_join_missing_count":total-ready,"sector_join_coverage":cov,"sector_join_status":"READY" if cov>=0.70 else "PARTIAL" if cov>0 else "DATA_INSUFFICIENT","joined_rows_sample":joined[:100],"joined_rows":joined,"real_trade_allowed":False,"broker_order_allowed":False,"safety":dict(DEFAULT_SECTOR_CLOCK_SAFETY)}
