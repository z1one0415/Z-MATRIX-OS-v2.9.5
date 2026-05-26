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
    "HumanDiaryEvent",
    "MistakeAttributionEvent",
    "MemoryCandidateEvent",
    "CalibrationEvent",
    "HumanApprovalEvent",
    "PromptPatchEvent",
})

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
