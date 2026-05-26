"""Human Approval Decision — build approval decision with safe mapping"""
from __future__ import annotations
import hashlib
from datetime import datetime, timezone

DECISION_VERSION = "HUMAN_APPROVAL_DECISION_V10"

_DECISION_MAP = {
    "APPROVE": "APPROVED",
    "REJECT": "REJECTED",
    "QUARANTINE": "QUARANTINED",
    "REQUEST_MORE_EVIDENCE": "PENDING_REVIEW",
}

_DECISION_SAFETY = {
    "hermes_memory_write_allowed": False,
    "real_z9_write_allowed": False,
    "auto_calibration_allowed": False,
    "prompt_auto_injection_allowed": False,
    "real_trade_allowed": False,
    "local_event_write_allowed": True,
}


def build_human_approval_decision(
    *,
    approval_request: dict,
    decision: str,
    human_operator: str,
    rationale: str,
) -> dict:
    """Build a HumanApprovalDecision.

    Mapping:
    - APPROVE → APPROVED
    - REJECT → REJECTED
    - QUARANTINE → QUARANTINED
    - REQUEST_MORE_EVIDENCE → PENDING_REVIEW

    Critical boundary:
    APPROVE represents 'human approval record established'.
    It does NOT enable Hermes memory write, auto calibration,
    or prompt auto injection.
    """
    if decision not in _DECISION_MAP:
        raise ValueError(f"Invalid decision '{decision}'. Must be one of {list(_DECISION_MAP.keys())}")

    seed = f"{approval_request.get('approval_request_id','')}|{decision}|{human_operator}"
    decision_id = hashlib.sha256(seed.encode()).hexdigest()[:32]
    created_at = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    return {
        "approval_decision_id": decision_id,
        "decision_version": DECISION_VERSION,
        "approval_request_id": approval_request.get("approval_request_id", ""),
        "source_preview_id": approval_request.get("source_preview_id", ""),
        "decision": decision,
        "result_status": _DECISION_MAP[decision],
        "human_operator": human_operator,
        "rationale": rationale,
        "created_at": created_at,
        "safety": dict(_DECISION_SAFETY),
    }
