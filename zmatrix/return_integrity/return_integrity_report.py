from __future__ import annotations
from zmatrix.return_integrity.robust_metrics import build_robust_return_metrics
from zmatrix.return_integrity.outlier_attribution import build_outlier_attribution
from zmatrix.return_integrity.role_performance import build_role_performance_report
from zmatrix.return_integrity.strategy_verdict import build_strategy_verdict
from zmatrix.return_integrity.policy import validate_return_integrity_report

def build_return_integrity_report(*, outcomes: list[dict], paper_actions: list[dict], audit_report: dict | None = None, horizon: str = "t20") -> dict:
    robust = build_robust_return_metrics(outcomes=outcomes, horizon=horizon)
    outliers = build_outlier_attribution(outcomes=outcomes, paper_actions=paper_actions, horizon=horizon)
    role_perf = build_role_performance_report(outcomes=outcomes, paper_actions=paper_actions, horizon=horizon)
    verdict = build_strategy_verdict(robust_metrics=robust, audit_report=audit_report)
    report = {"report_version": "V36_RETURN_INTEGRITY_REPORT_V10", "mode": "ANALYSIS_ONLY", "horizon": horizon.upper(), "robust_metrics": robust, "outlier_attribution": outliers, "role_performance": role_perf, "strategy_verdict": verdict, "audit_report_ref": {"audit_status": (audit_report or {}).get("audit_status"), "active_paper_actions": (audit_report or {}).get("active_outcome_validation", {}).get("active_paper_actions"), "ready_outcomes": (audit_report or {}).get("active_outcome_validation", {}).get("ready_outcomes")}, "real_trade_allowed": False, "broker_order_allowed": False, "auto_buy_allowed": False, "auto_sell_allowed": False, "auto_position_close_allowed": False, "real_z9_write_allowed": False, "hermes_memory_write_allowed": False, "auto_calibration_allowed": False, "runtime_enabled": False}
    report["policy_violations"] = validate_return_integrity_report(report)
    return report
