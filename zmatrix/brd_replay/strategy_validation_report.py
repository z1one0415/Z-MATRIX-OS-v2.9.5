# allowlist: forbidden-token-definition
"""Strategy Validation Report — aggregate all v3.2 replay results (v3.3 update)"""
from __future__ import annotations
from zmatrix.brd_replay.metrics import build_strategy_metrics
from zmatrix.brd_replay.role_stats import build_role_stats
from zmatrix.brd_replay.sector_phase_stats import build_sector_phase_stats


def build_brd_strategy_validation_report(*, replay_result, horizon="t20"):
    all_actions, all_outcomes = [], []
    for daily in replay_result.get("daily_results", []):
        all_actions.extend(daily.get("paper_actions", []))
        all_outcomes.extend(daily.get("outcomes", []))

    brd_connected = any(
        x.get("source_brd_result", {}).get("brd_connected") is True
        for x in all_actions if x.get("source_brd_result")
    )
    fallback_count = sum(
        1 for x in all_actions
        if x.get("source_brd_result", {}).get("fallback") is True
    )
    fallback_rate = fallback_count / len(all_actions) if all_actions else None

    validation_status = (
        "BRD_CONNECTED_STRATEGY_VALIDATION_READY"
        if brd_connected and (fallback_rate is None or fallback_rate < 0.05)
        else "FRAMEWORK_READY_BRD_NOT_CONNECTED"
    )

    return {
        "report_version": "BRD_STRATEGY_VALIDATION_REPORT_V10",
        "mode": "REPORT_ONLY",
        "horizon": horizon.upper(),
        "date_count": replay_result.get("date_count"),
        "success_day_count": replay_result.get("success_day_count"),
        "total_paper_actions": len(all_actions),
        "total_outcomes": len(all_outcomes),
        "overall_metrics": build_strategy_metrics(outcomes=all_outcomes, horizon=horizon),
        "role_stats": build_role_stats(paper_actions=all_actions, outcomes=all_outcomes, horizon=horizon),
        "sector_phase_stats": build_sector_phase_stats(paper_actions=all_actions, outcomes=all_outcomes, horizon=horizon),
        "brd_connected": brd_connected,
        "fallback_count": fallback_count,
        "fallback_rate": fallback_rate,
        "validation_status": validation_status,
        "known_limitations": ["Historical replay is paper-only.", "No broker.", "No real trade.", "No runtime.", "No auto Z9."],
        "real_trade_allowed": False, "broker_order_allowed": False, "runtime_enabled": False,
    }
