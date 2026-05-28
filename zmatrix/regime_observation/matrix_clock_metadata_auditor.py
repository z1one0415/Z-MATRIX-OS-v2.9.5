from __future__ import annotations
from zmatrix.regime_observation.schema import DEFAULT_REGIME_OBSERVATION_SAFETY

def _has_meta(x):
    if not isinstance(x,dict): return False
    return bool(x.get("as_of_date") or x.get("updated_at") or x.get("timestamp"))

def audit_matrix_clock_metadata(*, rows: list[dict]) -> dict:
    t=len(rows or []); b=r=d=0
    for row in rows or []:
        s = row.get("source_brd_result",{}) or {}; raw = s.get("source_raw",{}) or {}
        if _has_meta(raw.get("b_matrix") or s.get("b_matrix") or {}): b+=1
        if _has_meta(raw.get("r_matrix") or s.get("r_matrix") or {}): r+=1
        if _has_meta(raw.get("d_matrix") or s.get("d_matrix") or {}): d+=1
    bc = b/t if t else 0; rc = r/t if t else 0; dc = d/t if t else 0
    ready = bc>=0.70 and rc>=0.70 and dc>=0.70
    return {"auditor_version":"V358_MATRIX_CLOCK_METADATA_AUDIT_V10","matrix_clock_status":"MATRIX_CLOCK_READY" if ready else "MATRIX_CLOCK_DATA_INSUFFICIENT","total_rows":t,"b_meta_coverage":bc,"r_meta_coverage":rc,"d_meta_coverage":dc,"data_decay_penalty_required":not ready,"production_weight_adjustment_allowed":False,"real_trade_allowed":False,"broker_order_allowed":False,"safety":dict(DEFAULT_REGIME_OBSERVATION_SAFETY)}
