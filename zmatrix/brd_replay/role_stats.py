# allowlist: forbidden-token-definition
"""Role Stats — per-role A/B/C/D performance"""
from __future__ import annotations
from zmatrix.brd_replay.metrics import build_strategy_metrics

def build_role_stats(*, paper_actions, outcomes, horizon="t20"):
    by_id = {x.get("paper_id"):x for x in paper_actions}
    grouped = {}
    for o in outcomes:
        role = by_id.get(o.get("paper_id"),{}).get("role","UNKNOWN")
        grouped.setdefault(role,[]).append(o)
    stats = {r:build_strategy_metrics(outcomes=outs,horizon=horizon) for r,outs in grouped.items()}
    return {"role_stats_version":"BRD_ROLE_STATS_V10","horizon":horizon.upper(),"roles":stats,"role_count":len(stats),
            "real_trade_allowed":False,"broker_order_allowed":False}
