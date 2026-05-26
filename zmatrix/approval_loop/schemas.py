"""Approval Loop schemas — types, statuses, safety"""
from __future__ import annotations

APPROVAL_REQUEST_TYPES = frozenset({
    "MEMORY_CANDIDATE_APPROVAL",
    "CALIBRATION_EVENT_APPROVAL",
    "PROMPT_PATCH_APPROVAL",
})

APPROVAL_STATUS = frozenset({
    "DRAFT", "PENDING_REVIEW", "APPROVED", "REJECTED",
    "QUARANTINED", "EXPIRED", "SUPERSEDED",
})

APPROVAL_DECISION_TYPES = frozenset({
    "APPROVE", "REJECT", "QUARANTINE", "REQUEST_MORE_EVIDENCE",
})

DEFAULT_APPROVAL_SAFETY = {
    "real_trade_allowed": False,
    "broker_order_allowed": False,
    "real_z9_write_allowed": False,
    "hermes_memory_write_allowed": False,
    "auto_calibration_allowed": False,
    "prompt_auto_injection_allowed": False,
    "approval_required": True,
    "local_event_write_allowed": True,
}
