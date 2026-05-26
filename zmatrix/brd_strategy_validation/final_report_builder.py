"""Final Report Builder — aggregate all v3.5 validation results"""
from __future__ import annotations
from zmatrix.brd_strategy_validation.role_breakdown import build_role_breakdown
from zmatrix.brd_strategy_validation.phase_breakdown import build_phase_breakdown
from zmatrix.brd_strategy_validation.validation_policy import validate_v35_report_safety

def build_v35_final_validation_report(*, validation_result, replay_result, horizon="t20"):
    role = build_role_breakdown(replay_result=replay_result, horizon=horizon)
    phase = build_phase_breakdown(replay_result=replay_result, horizon=horizon)
    report = {"report_version":"V35_FINAL_BRD_STRATEGY_VALIDATION_REPORT_V10","mode":"REPORT_ONLY",
        "validation_status":validation_result.get("validation_status"),"horizon":horizon.upper(),
        "date_count":validation_result.get("date_count"),"brd_connected":validation_result.get("brd_connected"),
        "fallback_rate":validation_result.get("fallback_rate"),
        "metrics":validation_result.get("metrics",{}),
        "role_breakdown":role,"phase_breakdown":phase,
        "failure_analysis":validation_result.get("failure_analysis",{}),
        "known_limitations":["paper-only historical validation","no live trading","no broker","no Z9","no Hermes","no runtime"],
        "real_trade_allowed":False,"broker_order_allowed":False,"auto_buy_allowed":False,"auto_sell_allowed":False,
        "auto_position_close_allowed":False,"real_z9_write_allowed":False,"hermes_memory_write_allowed":False,
        "auto_calibration_allowed":False,"runtime_enabled":False}
    report["policy_violations"] = validate_v35_report_safety(report)
    return report
