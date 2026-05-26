"""Sector Phase Stats — per-phase performance"""
from __future__ import annotations
from zmatrix.brd_replay.metrics import build_strategy_metrics

def build_sector_phase_stats(*, paper_actions, outcomes, horizon="t20"):
    by_id = {x.get("paper_id"):x for x in paper_actions}
    grouped = {}
    for o in outcomes:
        phase = by_id.get(o.get("paper_id"),{}).get("sector_phase","UNKNOWN")
        grouped.setdefault(phase,[]).append(o)
    stats = {p:build_strategy_metrics(outcomes=outs,horizon=horizon) for p,outs in grouped.items()}
    return {"sector_phase_stats_version":"BRD_SECTOR_PHASE_STATS_V10","horizon":horizon.upper(),"phases":stats,
            "phase_count":len(stats),"real_trade_allowed":False,"broker_order_allowed":False}
