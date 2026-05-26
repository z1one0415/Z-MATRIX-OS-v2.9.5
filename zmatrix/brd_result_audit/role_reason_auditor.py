"""Role Reason Auditor — verify active roles have explainable reason_codes"""
from __future__ import annotations
from zmatrix.brd_result_audit.schema import DEFAULT_AUDIT_SAFETY

def audit_role_reason_integrity(*, paper_actions):
    violations=[]; checked=0
    for a in (paper_actions or[]):
        role=a.get("role")
        if role not in ("A_LONG_CORE","B_MID_ROTATION","C_SHORT_EVENT"): continue
        checked+=1
        brd=a.get("source_brd_result",{}) or {}
        b=brd.get("source_raw",{}).get("b_matrix") or brd.get("b_matrix") or {}
        rcs=b.get("reason_codes",[]) or brd.get("reason_codes",[])
        if not rcs: violations.append({"ticker":a.get("ticker"),"role":role,"issue":"ACTIVE_ROLE_MISSING_REASON_CODES"})
        if role=="A_LONG_CORE" and b.get("role_cap") and b["role_cap"]!="A_LONG_CORE":
            violations.append({"ticker":a.get("ticker"),"role":role,"role_cap":b["role_cap"],"issue":"ROLE_EXCEEDS_B_MATRIX_ROLE_CAP"})
    return {"audit_version":"ROLE_REASON_INTEGRITY_AUDIT_V10","checked_active_roles":checked,
            "violation_count":len(violations),"violations":violations[:100],"pass":len(violations)==0,
            "safety":dict(DEFAULT_AUDIT_SAFETY),"real_trade_allowed":False,"broker_order_allowed":False}
