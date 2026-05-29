# allowlist: forbidden-token-definition
"""Prompt Middleware schemas — types, statuses, safety defaults"""
from __future__ import annotations

PROMPT_PATCH_REQUEST_TYPES = frozenset({
    "TASK_DISCIPLINE_PATCH",
    "RISK_CAUTION_PATCH",
    "ROLE_REVIEW_PATCH",
    "OUTCOME_REVIEW_PATCH",
    "UNKNOWN",
})

PROMPT_PATCH_STATUS = frozenset({
    "DRAFT", "PENDING_APPROVAL", "APPROVED_PREVIEW",
    "REJECTED", "QUARANTINED", "EXPIRED",
})

PROMPT_RENDER_MODE = frozenset({"PREVIEW_ONLY"})

DEFAULT_PROMPT_MIDDLEWARE_SAFETY = {
    "real_trade_allowed": False,
    "broker_order_allowed": False,
    "real_z9_write_allowed": False,
    "hermes_memory_write_allowed": False,
    "auto_calibration_allowed": False,
    "prompt_auto_injection_allowed": False,
    "system_prompt_write_allowed": False,
    "runtime_injection_allowed": False,
    "requires_human_approval": True,
    "local_event_write_allowed": True,
}
