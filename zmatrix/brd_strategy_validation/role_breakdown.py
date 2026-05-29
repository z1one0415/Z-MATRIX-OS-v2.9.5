# allowlist: forbidden-token-definition
"""Role Breakdown — per-role A/B/C/D performance, excludes NO_ACTION/DATA_GAP"""
from __future__ import annotations
from zmatrix.brd_strategy_validation.metrics_aggregator import _metric_for_horizon

def build_role_breakdown(*, replay_result, horizon="t20"):
    actions, outcomes = [], []
    for daily in replay_result.get("daily_results",[]):
        actions.extend(daily.get("paper_actions",[]))
        outcomes.extend(daily.get("outcomes",[]))
    by_id = {a.get("paper_id"):a for a in actions}
    grouped = {}
    for o in outcomes:
        pid = o.get("paper_id")
        act = by_id.get(pid,{})
        if act.get("paper_action") in ("NO_ACTION","DATA_GAP"): continue
        role = act.get("role","UNKNOWN")
        grouped.setdefault(role,[]).append(o)
    stats = {r:_metric_for_horizon(outs,horizon) for r,outs in grouped.items()}
    return {"role_breakdown_version":"V35_ROLE_BREAKDOWN_V10","horizon":horizon.upper(),
            "role_count":len(stats),"roles":stats,"real_trade_allowed":False,"broker_order_allowed":False}
