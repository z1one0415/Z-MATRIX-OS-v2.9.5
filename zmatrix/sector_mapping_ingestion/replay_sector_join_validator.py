# allowlist: forbidden-token-definition
from __future__ import annotations
from zmatrix.sector_mapping_ingestion.schema import DEFAULT_SECTOR_MAPPING_SAFETY

def validate_replay_sector_join(*, replay_rows: list[dict], sector_mapping: dict) -> dict:
    total = len(replay_rows or []); ready = 0; missing = []
    for row in replay_rows or []:
        tk = str(row.get("ticker") or "").split(".")[0].zfill(6)
        if tk in sector_mapping and sector_mapping[tk].get("sector"): ready+=1
        else: missing.append(tk)
    cov = ready/total if total else 0
    status = "READY" if cov>=0.90 else "PARTIAL" if cov>0 else "DATA_INSUFFICIENT"
    return {"join_validator_version":"V3510_REPLAY_SECTOR_JOIN_VALIDATOR_V10","join_status":status,"replay_row_count":total,"join_ready_count":ready,"join_missing_count":total-ready,"join_coverage":cov,"missing_tickers_sample":missing[:100],"real_trade_allowed":False,"broker_order_allowed":False,"safety":dict(DEFAULT_SECTOR_MAPPING_SAFETY)}
