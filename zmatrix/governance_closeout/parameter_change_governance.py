from __future__ import annotations
from zmatrix.governance_closeout.schema import DEFAULT_GOVERNANCE_SAFETY

def build_parameter_change_governance(*, yaml_audit: dict) -> dict:
    changed = yaml_audit.get("sensitive_changed_files",[]); detected = bool(changed)
    return {"governance_version":"V357_PARAMETER_CHANGE_GOVERNANCE_V10","parameter_change_detected":detected,"sensitive_changed_files":changed,"causal_rationale_required":detected,"human_approval_required":detected,"rollback_plan_required":detected,"auto_merge_allowed":False,"production_write_allowed":False,"z9_auto_calibration_write_allowed":False,"required_rationale_fields":["parameter_change_reason","causal_hypothesis","evidence_source","anti_overfit_result","expected_failure_mode","rollback_plan","human_approval_record"] if detected else [],"governance_status":"PARAMETER_CHANGE_REQUIRES_HUMAN_APPROVAL" if detected else "NO_PARAMETER_CHANGE","real_trade_allowed":False,"broker_order_allowed":False,"safety":dict(DEFAULT_GOVERNANCE_SAFETY)}
