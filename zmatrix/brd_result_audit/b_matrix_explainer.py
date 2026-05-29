# allowlist: forbidden-token-definition
"""B-Matrix Explainer — human-readable explanation of B-Matrix results"""
from __future__ import annotations
from zmatrix.brd_result_audit.schema import DEFAULT_AUDIT_SAFETY

def explain_b_matrix_result(*, ticker, b_matrix):
    rc=list(b_matrix.get("reason_codes",[]))
    dg=b_matrix.get("downgrade",{}) or {}
    dq=b_matrix.get("data_quality",{}) or {}
    explanation=[f"status={b_matrix.get('status')}",f"quality={b_matrix.get('quality_score')}","growth={b_matrix.get('growth_score')}"]
    if b_matrix.get("valuation_data_status"): explanation.append(f"val_status={b_matrix['valuation_data_status']}")
    if dg.get("downgraded"): explanation.append(f"cap {dg.get('from_role_cap')}→{dg.get('to_role_cap')} ({dg.get('downgrade_reason')})")
    return {"explain_version":"B_MATRIX_EXPLAIN_V10","ticker":ticker,"b_status":b_matrix.get("status"),
            "b_score":b_matrix.get("b_score"),"quality_score":b_matrix.get("quality_score"),"growth_score":b_matrix.get("growth_score"),
            "valuation_score":b_matrix.get("valuation_score"),"valuation_data_status":b_matrix.get("valuation_data_status"),
            "valuation_confidence":b_matrix.get("valuation_confidence"),"valuation_method":b_matrix.get("valuation_method"),
            "role_cap":b_matrix.get("role_cap"),"downgrade":dg,"data_quality":dq,"reason_codes":rc,
            "human_readable_explanation":explanation,"safety":dict(DEFAULT_AUDIT_SAFETY),"real_trade_allowed":False,"broker_order_allowed":False}
