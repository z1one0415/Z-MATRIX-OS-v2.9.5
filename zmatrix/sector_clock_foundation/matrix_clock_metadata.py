# allowlist: forbidden-token-definition
from __future__ import annotations
from datetime import datetime
from zmatrix.sector_clock_foundation.schema import DEFAULT_SECTOR_CLOCK_SAFETY, CLOCK_DEFAULT_TTL

def _pd(x):
    if not x: return None
    s = str(x).replace("-","")[:8]
    try: return datetime.strptime(s,"%Y%m%d")
    except: return None

def build_matrix_clock_metadata(*, matrix_type: str, matrix_name: str, as_of_date: str | None, updated_at: str | None = None, source_table: str | None = None) -> dict:
    mt = matrix_type.upper(); ttl = CLOCK_DEFAULT_TTL.get(mt); dt = _pd(as_of_date or updated_at)
    return {"metadata_version":"V359_MATRIX_CLOCK_METADATA_V10","matrix_type":mt,"matrix_name":matrix_name,"as_of_date":as_of_date,"updated_at":updated_at,"source_table":source_table,"ttl_days":ttl,"age_days":None,"freshness_status":"MISSING" if dt is None else "FRESH","metadata_ready":dt is not None and ttl is not None,"real_trade_allowed":False,"broker_order_allowed":False,"safety":dict(DEFAULT_SECTOR_CLOCK_SAFETY)}

def evaluate_matrix_freshness(*, metadata: dict, current_date: str) -> dict:
    dt = _pd(metadata.get("as_of_date") or metadata.get("updated_at")); cur = _pd(current_date); ttl = metadata.get("ttl_days")
    age = (cur-dt).days if dt and cur else None
    status = "MISSING" if dt is None or ttl is None else "STALE" if age > ttl else "FRESH"
    out = dict(metadata); out.update({"age_days":age,"freshness_status":status,"data_decay_penalty_required":status in ("MISSING","STALE")}); return out
