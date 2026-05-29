# allowlist: forbidden-token-definition
"""EventStore schemas — base event fields, event types, safety fields"""
from __future__ import annotations

BASE_EVENT_FIELDS = [
    "event_id",
    "event_type",
    "schema_version",
    "created_at",
    "producer_module",
    "source_event_id",
    "parent_event_id",
    "input_hash",
    "output_hash",
    "payload",
    "safety",
]

EVENT_TYPES = frozenset({
    "ResearchEvent",
    "CandidateReviewEvent",
    "RoleClassificationEvent",
    "PaperDecisionEvent",
    "PaperLedgerEvent",
    "OutcomeBackfillEvent",
    "RiskEvent",
# RiskEvent may record tail-risk gate preview, controller preview, or risk isolation preview.
# It does not imply broker order.
# It does not imply auto sell.
# It does not imply position close.
# It does not imply real trade.
    "HumanDiaryEvent",
    "MistakeAttributionEvent",
    "MemoryCandidateEvent",
    "CalibrationEvent",
    "HumanApprovalEvent",
    "PromptPatchEvent",
    "ApprovalRequestEvent",
})

# PromptPatchEvent may record prompt patch request/render/audit preview.
# It does not imply system_prompt write.
# It does not imply runtime injection.
# It does not imply prompt auto injection.

# ApprovalRequestEvent records approval requests only.
# It does not imply human approval.
# It does not imply Hermes memory write.
# It does not imply auto calibration.
# It does not imply prompt injection.
#
# HumanApprovalEvent = human approval decision record
# ApprovalRequestEvent = approval request record
# MemoryCandidateEvent = memory candidate record
# Three types must NOT be mixed.

SAFETY_FIELDS = [
    "real_trade_allowed",
    "broker_order_allowed",
    "real_z9_write_allowed",
    "hermes_memory_write_allowed",
    "auto_calibration_allowed",
    "prompt_auto_injection_allowed",
    "local_event_write_allowed",
]

DEFAULT_EVENT_SAFETY = {
    "real_trade_allowed": False,
    "broker_order_allowed": False,
    "real_z9_write_allowed": False,
    "hermes_memory_write_allowed": False,
    "auto_calibration_allowed": False,
    "prompt_auto_injection_allowed": False,
    "local_event_write_allowed": True,
}

SCHEMA_VERSION = "EVENT_STORE_V10"
