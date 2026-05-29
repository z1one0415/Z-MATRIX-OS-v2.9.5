# allowlist: forbidden-token-definition
from __future__ import annotations
from datetime import datetime
from zmatrix.governance_closeout.schema import DEFAULT_GOVERNANCE_SAFETY, MATRIX_CLOCK_THRESHOLDS

def _pd(x):
    if not x: return None
    s=str(x).replace("-","")[:8]
    try: return datetime.strptime(s,"%Y%m%d")
    except: return None

def precheck_matrix_clock_alignment(*, b_matrix_meta=None, r_matrix_meta=None, d_matrix_meta=None, as_of_date=None) -> dict:
    meta = {"B":b_matrix_meta or {},"R":r_matrix_meta or {},"D":d_matrix_meta or {}}
    aof = _pd(as_of_date); fresh = {}; missing = []
    for k,m in meta.items():
        dt = _pd(m.get("as_of_date") or m.get("updated_at") or m.get("timestamp"))
        if dt is None or aof is None: missing.append(k); fresh[k]={"status":"DATA_INSUFFICIENT","age_days":None}
        else:
            age = (aof-dt).days; ttl = MATRIX_CLOCK_THRESHOLDS[f"{k.lower()}_matrix_ttl_days"]
            fresh[k]={"status":"STALE" if age>ttl else "FRESH","age_days":age,"ttl_days":ttl}
    status = "DATA_INSUFFICIENT" if missing else "CLOCK_ALIGNMENT_WARNING" if any(x["status"]=="STALE" for x in fresh.values()) else "CLOCK_ALIGNMENT_PASS"
    return {"precheck_version":"V357_MATRIX_CLOCK_ALIGNMENT_PRECHECK_V10","clock_alignment_status":status,"freshness":fresh,"missing_matrix_metadata":missing,"data_decay_penalty_required":status in ("DATA_INSUFFICIENT","CLOCK_ALIGNMENT_WARNING"),"production_weight_adjustment_allowed":False,"real_trade_allowed":False,"broker_order_allowed":False,"safety":dict(DEFAULT_GOVERNANCE_SAFETY)}
