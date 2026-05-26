"""Hermes Memory Kernel schemas — field definitions, status enums, safety defaults"""
from __future__ import annotations

CORE_MEMORY_FIELDS = [
    "memory_id",
    "memory_type",
    "title",
    "content",
    "priority",
    "source",
    "created_at",
    "valid_until",
    "status",
]

WORKING_CONTEXT_FIELDS = [
    "context_id",
    "context_type",
    "ticker",
    "chain",
    "sector",
    "role",
    "event_ids",
    "summary",
    "created_at",
]

LEARNED_HEURISTIC_FIELDS = [
    "heuristic_id",
    "source_event_id",
    "title",
    "rule",
    "scope",
    "confidence",
    "evidence_count",
    "last_validated_at",
    "status",
]

MEMORY_CANDIDATE_FIELDS = [
    "candidate_id",
    "source_event_id",
    "candidate_type",
    "title",
    "proposed_rule",
    "evidence_summary",
    "confidence",
    "risk_of_overfitting",
    "approval_status",
    "created_at",
]

PROMPT_PATCH_PREVIEW_FIELDS = [
    "patch_id",
    "source_heuristic_ids",
    "task_type",
    "ticker",
    "role",
    "patch_text",
    "preview_only",
    "prompt_auto_injection_allowed",
]

MEMORY_STATUS = frozenset({
    "ACTIVE", "STALE", "EXPIRED", "REJECTED", "QUARANTINED",
})

APPROVAL_STATUS = frozenset({
    "DRAFT", "PENDING_REVIEW", "APPROVED", "REJECTED", "QUARANTINED",
})

HERMES_KERNEL_SAFETY = {
    "read_only": True,
    "write_allowed": False,
    "hermes_memory_write_allowed": False,
    "real_z9_write_allowed": False,
    "auto_calibration_allowed": False,
    "prompt_auto_injection_allowed": False,
    "real_trade_allowed": False,
    "preview_only": True,
}
