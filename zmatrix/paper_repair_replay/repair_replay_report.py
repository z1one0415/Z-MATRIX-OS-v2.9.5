from __future__ import annotations
from zmatrix.paper_repair_replay.repaired_return_calculator import build_repaired_outcomes
from zmatrix.paper_repair_replay.baseline_repair_comparator import compare_baseline_vs_repaired
from zmatrix.paper_repair_replay.policy import validate_paper_repair_replay_report
from zmatrix.paper_repair_replay.schema import DEFAULT_REPAIR_REPLAY_SAFETY

def build_paper_repair_replay_report(*, joined: list[dict], data_root: str = ".", horizon_days: int = 20, max_items: int | None = None) -> dict:
    repaired = build_repaired_outcomes(joined=joined, data_root=data_root, horizon_days=horizon_days, max_items=max_items)
    comparison = compare_baseline_vs_repaired(repaired_result=repaired)
    report = {"report_version": "V353_PAPER_REPAIR_REPLAY_REPORT_V10", "mode": "PAPER_ONLY_REPAIR_REPLAY", "repair_rule": "apply_invalidation_exit_rule", "horizon_days": horizon_days, "repaired_outcomes": {"input_count": repaired.get("input_count"), "ready_count": repaired.get("ready_count"), "ready_rate": repaired.get("ready_rate")}, "comparison": comparison, "sample_rows": repaired.get("rows", [])[:50], "lookahead_safe": True, "production_strategy_modified": False, "safety": dict(DEFAULT_REPAIR_REPLAY_SAFETY), "real_trade_allowed": False, "broker_order_allowed": False, "auto_buy_allowed": False, "auto_sell_allowed": False, "auto_position_close_allowed": False, "runtime_enabled": False}
    report["policy_violations"] = validate_paper_repair_replay_report(report)
    return report
