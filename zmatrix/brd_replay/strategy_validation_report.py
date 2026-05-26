"""Strategy Validation Report — aggregate all v3.2 replay results"""
from __future__ import annotations
from zmatrix.brd_replay.metrics import build_strategy_metrics
from zmatrix.brd_replay.role_stats import build_role_stats
from zmatrix.brd_replay.sector_phase_stats import build_sector_phase_stats

def build_brd_strategy_validation_report(*, replay_result, horizon="t20"):
    all_actions, all_outcomes = [], []
    for daily in replay_result.get("daily_results",[]):
        all_actions.extend(daily.get("paper_actions",[]))
        all_outcomes.extend(daily.get("outcomes",[]))
    brd_connected = not all(
        a.get("source_brd_result",{}).get("fallback_reason") in ("BRD_NOT_CONNECTED","brd_classifier_unavailable")
        for a in all_actions if a.get("source_brd_result"))
    return {"report_version":"BRD_STRATEGY_VALIDATION_REPORT_V10","mode":"REPORT_ONLY",
            "horizon":horizon.upper(),"date_count":replay_result.get("date_count"),
            "success_day_count":replay_result.get("success_day_count"),
            "total_paper_actions":len(all_actions),"total_outcomes":len(all_outcomes),
            "overall_metrics":build_strategy_metrics(outcomes=all_outcomes,horizon=horizon),
            "role_stats":build_role_stats(paper_actions=all_actions,outcomes=all_outcomes,horizon=horizon),
            "sector_phase_stats":build_sector_phase_stats(paper_actions=all_actions,outcomes=all_outcomes,horizon=horizon),
            "brd_connected":brd_connected,
            "known_limitations":["Historical replay is paper-only.","No broker.","No real trade.","No runtime.","No auto Z9."],
            "real_trade_allowed":False,"broker_order_allowed":False,"runtime_enabled":False}
