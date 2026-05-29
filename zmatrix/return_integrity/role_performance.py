# allowlist: forbidden-token-definition
from __future__ import annotations
from zmatrix.return_integrity.robust_metrics import build_robust_return_metrics

def build_role_performance_report(*, outcomes: list[dict], paper_actions: list[dict], horizon: str = "t20") -> dict:
    action_by_id = {a.get("paper_id"): a for a in paper_actions or []}
    grouped = {}
    for o in outcomes or []:
        action = action_by_id.get(o.get("paper_id"), {})
        role = action.get("role", "UNKNOWN")
        paper_action = action.get("paper_action")
        if role == "D_REJECT":
            continue
        if paper_action in ("NO_ACTION", "DATA_GAP", None):
            continue
        grouped.setdefault(role, []).append(o)
    return {"report_version": "ROLE_PERFORMANCE_V10", "horizon": horizon.upper(), "roles": {role: build_robust_return_metrics(outcomes=outs, horizon=horizon) for role, outs in grouped.items()}, "real_trade_allowed": False, "broker_order_allowed": False}
