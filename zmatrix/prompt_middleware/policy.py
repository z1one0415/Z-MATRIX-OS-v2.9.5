"""Prompt Middleware Policy — validate requests, renders, audits, and safety"""
from __future__ import annotations

from zmatrix.prompt_middleware.schemas import PROMPT_PATCH_REQUEST_TYPES

_BLOCKED_FIELDS = [
    "runtime_injection_allowed",
    "system_prompt_write_allowed",
    "prompt_auto_injection_allowed",
    "hermes_memory_write_allowed",
    "real_z9_write_allowed",
    "auto_calibration_allowed",
    "real_trade_allowed",
]


def validate_prompt_patch_request(request: dict) -> list[str]:
    """Validate a PromptPatchRequest's structure and safety."""
    violations = []

    if not request.get("prompt_patch_request_id"):
        violations.append("prompt_patch_request_id required")
    if request.get("request_type") not in PROMPT_PATCH_REQUEST_TYPES:
        violations.append(f"invalid request_type: {request.get('request_type')}")
    if request.get("status") not in ("PENDING_APPROVAL", "APPROVED_PREVIEW", "REJECTED", "QUARANTINED", "EXPIRED"):
        violations.append(f"invalid status: {request.get('status')}")
    if not request.get("prompt_patch_preview_id"):
        violations.append("prompt_patch_preview_id required")
    if not request.get("task_context"):
        violations.append("task_context required/empty")

    safety = request.get("safety", {})
    if not isinstance(safety, dict):
        violations.append("safety must be dict")

    return violations + assert_no_prompt_runtime_effects(request)


def validate_prompt_render_preview(render: dict) -> list[str]:
    """Validate a rendered prompt middleware preview."""
    violations = []

    if render.get("mode") != "PREVIEW_ONLY":
        violations.append("mode must be PREVIEW_ONLY")
    if render.get("render_status") != "RENDERED_PREVIEW":
        violations.append("render_status must be RENDERED_PREVIEW")
    if not render.get("rendered_prompt_preview"):
        violations.append("rendered_prompt_preview required")

    return violations + assert_no_prompt_runtime_effects(render)


def validate_prompt_patch_audit(audit: dict) -> list[str]:
    """Validate a PromptPatchAudit record."""
    violations = []

    if not audit.get("prompt_patch_audit_id"):
        violations.append("prompt_patch_audit_id required")
    if not audit.get("render_id"):
        violations.append("render_id required")

    return violations + assert_no_prompt_runtime_effects(audit)


def assert_no_prompt_runtime_effects(record: dict) -> list[str]:
    """Check that record does NOT enable prompt runtime effects.

    Checks BOTH top-level fields AND safety nested fields.
    - top-level True → fails
    - safety nested True → fails
    - safety non-dict → fails
    - missing field → OK
    """
    violations = []

    # Check top-level
    for field in _BLOCKED_FIELDS:
        if record.get(field) is True:
            violations.append(f"top-level {field} must be False")

    # Check safety nested
    safety = record.get("safety", {})
    if not isinstance(safety, dict):
        violations.append("safety must be dict")
        safety = {}

    for field in _BLOCKED_FIELDS:
        if safety.get(field) is True:
            violations.append(f"safety.{field} must be False")

    return violations
