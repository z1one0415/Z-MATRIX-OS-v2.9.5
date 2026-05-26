"""Rehearsal Validator — validate v3.0-alpha dry-run rehearsal for safety"""
from __future__ import annotations

from zmatrix.dry_run.schemas import DRY_RUN_VERSION, DRY_RUN_STEPS


def validate_v3_alpha_dry_run_rehearsal(rehearsal: dict) -> dict:
    """Validate a v3.0-alpha dry-run rehearsal.

    Checks all steps exist, all artifacts present, all safety fields False.
    """
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
        elif key:
            artifact = artifacts[key]

    if not rehearsal.get("lineage"):
        violations.append("lineage is empty")

    # Step-specific checks
    ar = artifacts.get("approval_request", {})
    if ar.get("status") != "PENDING_REVIEW":
        violations.append("approval_request.status must be PENDING_REVIEW")

    hd = artifacts.get("human_approval_decision", {})
    if hd.get("result_status") != "APPROVED":
        violations.append("human_approval_decision.result_status must be APPROVED")
    if hd.get("safety", {}).get("hermes_memory_write_allowed") is True:
        violations.append("human_approval_decision must not enable Hermes memory write")

    pr = artifacts.get("prompt_patch_request", {})
    if pr.get("status") != "APPROVED_PREVIEW":
        violations.append("prompt_patch_request.status must be APPROVED_PREVIEW")

    rndr = artifacts.get("prompt_render_preview", {})
    if rndr.get("mode") != "PREVIEW_ONLY":
        violations.append("prompt_render_preview.mode must be PREVIEW_ONLY")
    if rndr.get("runtime_injection_allowed") is True:
        violations.append("prompt_render_preview must not enable runtime injection")
    if rndr.get("system_prompt_write_allowed") is True:
        violations.append("prompt_render_preview must not write system prompt")

    tr = artifacts.get("tail_risk_controller_preview", {})
    if tr.get("real_trade_allowed") is True:
        violations.append("tail_risk_controller_preview must not allow real trade")

    rr = artifacts.get("v3_alpha_readiness_report", {})
    if rr.get("alpha_runtime_allowed") is True:
        violations.append("v3_alpha_readiness_report must have alpha_runtime_allowed=False")
    if rr.get("real_trade_allowed") is True:
        violations.append("v3_alpha_readiness_report must have real_trade_allowed=False")

    # Global safety
    for field in [
        "real_trade_allowed", "broker_order_allowed", "real_z9_write_allowed",
        "hermes_memory_write_allowed", "auto_calibration_allowed",
        "prompt_auto_injection_allowed", "system_prompt_write_allowed", "runtime_enabled",
    ]:
        if rehearsal.get(field) is True:
            violations.append(f"rehearsal.{field} must be False")

    safety = rehearsal.get("safety", {})
    for field in [
        "real_trade_allowed", "broker_order_allowed", "auto_buy_allowed",
        "auto_sell_allowed", "auto_position_close_allowed", "real_z9_write_allowed",
        "hermes_memory_write_allowed", "auto_calibration_allowed",
        "prompt_auto_injection_allowed", "system_prompt_write_allowed",
        "runtime_injection_allowed", "runtime_enabled", "external_api_default_on",
    ]:
        if safety.get(field) is True:
            violations.append(f"safety.{field} must be False")

    return {
        "validation_version": "V3_ALPHA_DRY_RUN_VALIDATION_V10",
        "pass": len(violations) == 0,
        "violations": violations,
        "dry_run_only": True,
        "real_trade_allowed": False,
        "runtime_enabled": False,
    }
