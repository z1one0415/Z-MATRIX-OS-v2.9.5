# allowlist: forbidden-token-definition
"""Phase Breakdown — per-sector-phase performance"""
from __future__ import annotations
from zmatrix.brd_strategy_validation.metrics_aggregator import _metric_for_horizon

def build_phase_breakdown(*, replay_result, horizon="t20"):
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
        phase = act.get("sector_phase","UNKNOWN")
        grouped.setdefault(phase,[]).append(o)
    stats = {p:_metric_for_horizon(outs,horizon) for p,outs in grouped.items()}
    return {"phase_breakdown_version":"V35_PHASE_BREAKDOWN_V10","horizon":horizon.upper(),
            "phase_count":len(stats),"phases":stats,"real_trade_allowed":False,"broker_order_allowed":False}
