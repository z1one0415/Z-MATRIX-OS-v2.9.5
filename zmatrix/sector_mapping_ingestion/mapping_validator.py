# allowlist: forbidden-token-definition
from __future__ import annotations
from zmatrix.sector_mapping_ingestion.schema import DEFAULT_SECTOR_MAPPING_SAFETY, MIN_READY_TICKERS, MIN_READY_COVERAGE, MIN_PARTIAL_COVERAGE

def validate_sector_mapping(*, sector_mapping: dict) -> dict:
    total = len(sector_mapping or {}); ready = sum(1 for x in (sector_mapping or {}).values() if x.get("sector"))
    cov = ready/total if total else 0
    status = "READY" if total>=MIN_READY_TICKERS and cov>=MIN_READY_COVERAGE else "PARTIAL" if total>0 and cov>=MIN_PARTIAL_COVERAGE else "DATA_INSUFFICIENT"
    sc = {}
    for x in (sector_mapping or {}).values():
        s = x.get("sector")
        if s: sc[s] = sc.get(s,0)+1
    return {"validator_version":"V3510_MAPPING_VALIDATOR_V10","sector_mapping_status":status,"ticker_count":total,"sector_ready_count":ready,"sector_missing_count":total-ready,"sector_coverage":cov,"sector_count":len(sc),"sector_counts_sample":dict(list(sc.items())[:30]),"real_trade_allowed":False,"broker_order_allowed":False,"safety":dict(DEFAULT_SECTOR_MAPPING_SAFETY)}
