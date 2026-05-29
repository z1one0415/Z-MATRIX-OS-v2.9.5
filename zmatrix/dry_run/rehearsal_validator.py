# allowlist: forbidden-token-definition
"""Rehearsal Validator — validate v3.0-alpha dry-run rehearsal for safety"""
from __future__ import annotations

from zmatrix.dry_run.schemas import DRY_RUN_VERSION, DRY_RUN_STEPS

_BLOCKED_SAFETY_FIELDS = [
    "real_trade_allowed", "broker_order_allowed", "auto_buy_allowed",
    "auto_sell_allowed", "auto_position_close_allowed", "real_z9_write_allowed",
    "hermes_memory_write_allowed", "auto_calibration_allowed",
    "prompt_auto_injection_allowed", "system_prompt_write_allowed",
    "runtime_injection_allowed", "runtime_enabled", "external_api_default_on",
]


def _check_blocked_fields(prefix: str, record: dict) -> list[str]:
    """Check both top-level and nested safety fields."""
    violations = []
    if not isinstance(record, dict):
        return violations

    for field in _BLOCKED_SAFETY_FIELDS:
        if record.get(field) is True:
            violations.append(f"{prefix}.{field} must be False")

    safety = record.get("safety", {})
    if safety is None:
        safety = {}
    if not isinstance(safety, dict):
        violations.append(f"{prefix}.safety must be dict")
        return violations

    for field in _BLOCKED_SAFETY_FIELDS:
        if safety.get(field) is True:
            violations.append(f"{prefix}.safety.{field} must be False")

    return violations


def validate_v3_alpha_dry_run_rehearsal(rehearsal: dict) -> dict:
    """Validate a v3.0-alpha dry-run rehearsal."""
    violations = []

    if rehearsal.get("dry_run_version") != DRY_RUN_VERSION:
        violations.append(f"invalid dry_run_version: {rehearsal.get('dry_run_version')}")
    if rehearsal.get("mode") != "DRY_RUN_ONLY":
        violations.append("mode must be DRY_RUN_ONLY")

    artifacts = rehearsal.get("artifacts", {})
    for step in DRY_RUN_STEPS:
        key = {
            "PaperLedgerEvent": "paper_ledger_event",
            "OutcomeBackfillEvent": "outcome_backfill_event",
            "MemoryCandidatePreview": "memory_candidate_preview",
            "ApprovalRequest": "approval_request",
            "HumanApprovalDecision": "human_approval_decision",
            "PromptPatchRequest": "prompt_patch_request",
            "PromptRenderPreview": "prompt_render_preview",
            "TailRiskControllerPreview": "tail_risk_controller_preview",
            "V3AlphaReadinessReport": "v3_alpha_readiness_report",
        }.get(step)
        if key and (key not in artifacts or not artifacts[key]):
            violations.append(f"artifact '{key}' missing or empty")

    if not rehearsal.get("lineage"):
        violations.append("lineage is empty")

    # Step-specific checks
    ar = artifacts.get("approval_request", {})
    if ar.get("status") != "PENDING_REVIEW":
        violations.append("approval_request.status must be PENDING_REVIEW")

    hd = artifacts.get("human_approval_decision", {})
    if hd.get("result_status") != "APPROVED":
        violations.append("human_approval_decision.result_status must be APPROVED")

    pr = artifacts.get("prompt_patch_request", {})
    if pr.get("status") != "APPROVED_PREVIEW":
        violations.append("prompt_patch_request.status must be APPROVED_PREVIEW")

    rndr = artifacts.get("prompt_render_preview", {})
    if rndr.get("mode") != "PREVIEW_ONLY":
        violations.append("prompt_render_preview.mode must be PREVIEW_ONLY")

    # Recursive artifact safety check
    violations.extend(_check_blocked_fields("rehearsal", rehearsal))
    for name, artifact in artifacts.items():
        violations.extend(_check_blocked_fields(f"artifacts.{name}", artifact))

    return {
        "validation_version": "V3_ALPHA_DRY_RUN_VALIDATION_V10",
        "pass": len(violations) == 0,
        "violations": violations,
        "dry_run_only": True,
        "real_trade_allowed": False,
        "runtime_enabled": False,
    }
