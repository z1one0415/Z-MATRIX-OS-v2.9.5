# allowlist: forbidden-token-definition
"""Audit Report Builder — aggregate all BRD result audits"""
from __future__ import annotations
from zmatrix.brd_result_audit.market_role_distribution import build_market_role_distribution_report
from zmatrix.brd_result_audit.role_reason_auditor import audit_role_reason_integrity
from zmatrix.brd_result_audit.active_outcome_validator import validate_active_outcomes
from zmatrix.brd_result_audit.audit_policy import validate_brd_result_audit_report

def build_brd_result_audit_report(*, replay_result):
    actions,outcomes=[],[]
    for daily in replay_result.get("daily_results",[]):
        actions.extend(daily.get("paper_actions",[])); outcomes.extend(daily.get("outcomes",[]))
    dist=build_market_role_distribution_report(paper_actions=actions)
    reason=audit_role_reason_integrity(paper_actions=actions)
    ao=validate_active_outcomes(paper_actions=actions,outcomes=outcomes)
    def _st(): return "BLOCKED_SMALL_SAMPLE" if dist["distribution_status"]=="SMALL_SAMPLE" else ("BLOCKED_REASON_INTEGRITY" if not reason["pass"] else (ao["status"] if ao["status"].startswith("BLOCKED") else "PASS"))
    report={"report_version":"BRD_RESULT_AUDIT_REPORT_V10","mode":"AUDIT_ONLY","market_role_distribution":dist,
            "role_reason_integrity":reason,"active_outcome_validation":ao,"audit_status":_st(),
            "real_trade_allowed":False,"broker_order_allowed":False,"auto_buy_allowed":False,"auto_sell_allowed":False,
            "auto_position_close_allowed":False,"real_z9_write_allowed":False,"hermes_memory_write_allowed":False,
            "auto_calibration_allowed":False,"runtime_enabled":False}
    report["policy_violations"]=validate_brd_result_audit_report(report)
    return report
