"""Approval Policy — validate requests, decisions, and safety boundaries"""
from __future__ import annotations

from zmatrix.approval_loop.schemas import APPROVAL_REQUEST_TYPES, APPROVAL_DECISION_TYPES

_DECISION_RESULT_MAP = {
    "APPROVE": "APPROVED",
    "REJECT": "REJECTED",
    "QUARANTINE": "QUARANTINED",
    "REQUEST_MORE_EVIDENCE": "PENDING_REVIEW",
}


def validate_approval_request(request: dict) -> list[str]:
    """Validate an approval request's structure and safety."""
    violations = []

    if not request.get("approval_request_id"):
        violations.append("approval_request_id required")
    if request.get("request_type") not in APPROVAL_REQUEST_TYPES:
        violations.append(f"invalid request_type: {request.get('request_type')}")
    if request.get("status") != "PENDING_REVIEW":
        violations.append("approval request status must be PENDING_REVIEW")
    if request.get("requires_human_approval") is not True:
        violations.append("requires_human_approval must be True")
    if not request.get("source_preview_id"):
        violations.append("source_preview_id required")
    if not request.get("source_preview_hash"):
        violations.append("source_preview_hash required")

    return violations + assert_no_auto_effects(request)


def validate_approval_decision(decision: dict) -> list[str]:
    """Validate an approval decision's structure and mapping consistency."""
    violations = []

    if not decision.get("approval_decision_id"):
        violations.append("approval_decision_id required")
    if not decision.get("approval_request_id"):
        violations.append("approval_request_id required")

    d = decision.get("decision")
    if d not in APPROVAL_DECISION_TYPES:
        violations.append(f"invalid decision: {d}")

    expected = _DECISION_RESULT_MAP.get(d)
    if expected and decision.get("result_status") != expected:
        violations.append(
            f"result_status must be {expected} for decision {d}, "
            f"got {decision.get('result_status')}"
        )

    return violations + assert_no_auto_effects(decision)


def assert_no_auto_effects(record: dict) -> list[str]:
    """Check that a record does NOT enable any automatic effects.

    Must check: real_trade, broker_order, real_z9_write,
    hermes_memory_write, auto_calibration, prompt_auto_injection.
    """
    violations = []
    safety = record.get("safety", {}) if isinstance(record.get("safety"), dict) else {}

    for field in [
        "real_trade_allowed", "broker_order_allowed", "real_z9_write_allowed",
        "hermes_memory_write_allowed", "auto_calibration_allowed",
        "prompt_auto_injection_allowed",
    ]:
        if safety.get(field) is True:
            violations.append(f"{field} must be False")

    # Also check top-level fields
    for field in [
        "real_trade_allowed", "hermes_memory_write_allowed",
        "auto_calibration_allowed", "prompt_auto_injection_allowed",
        "real_z9_write_allowed",
    ]:
        if record.get(field) is True:
            violations.append(f"top-level {field} must be False")

    return violations
