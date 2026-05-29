# allowlist: forbidden-token-definition
"""Active Outcome Validator — verify active paper actions have ready outcomes"""
from __future__ import annotations
from zmatrix.brd_result_audit.schema import DEFAULT_AUDIT_SAFETY

def validate_active_outcomes(*, paper_actions, outcomes):
    by_id={o.get("paper_id"):o for o in (outcomes or[])}
    active=[a for a in (paper_actions or[]) if a.get("paper_action") not in ("NO_ACTION","DATA_GAP",None)]
    ready=[]; missing=[]; insufficient=[]
    for a in active:
        pid=a.get("paper_id"); out=by_id.get(pid)
        if not out: missing.append({"paper_id":pid,"ticker":a.get("ticker"),"issue":"OUTCOME_MISSING"})
        elif out.get("outcome_status")=="READY": ready.append(out)
        else: insufficient.append({"paper_id":pid,"ticker":a.get("ticker"),"outcome_status":out.get("outcome_status"),"issue":"OUTCOME_NOT_READY"})
    ac=len(active); rc=len(ready)
    st="PASS" if ac>0 and rc>0 else ("BLOCKED_NO_ACTIVE_ACTIONS" if ac==0 else "BLOCKED_NO_READY_OUTCOMES")
    return {"validator_version":"ACTIVE_OUTCOME_VALIDATOR_V10","active_paper_actions":ac,"ready_outcomes":rc,
            "ready_outcome_rate":rc/ac if ac else None,"missing_outcome_count":len(missing),
            "insufficient_outcome_count":len(insufficient),"status":st,"missing_samples":missing[:30],
            "insufficient_samples":insufficient[:30],"safety":dict(DEFAULT_AUDIT_SAFETY),"real_trade_allowed":False,"broker_order_allowed":False}
