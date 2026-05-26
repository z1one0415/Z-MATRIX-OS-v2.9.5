"""Tag Readiness Validator — aggregate RC gate + artifact consistency for final tag review"""
from __future__ import annotations

from zmatrix.alpha_rc.rc_gate_validator import validate_v3_alpha_rc_gate
from zmatrix.alpha_tag.artifact_consistency import validate_alpha_rc_artifact_consistency
from zmatrix.alpha_tag.schemas import TARGET_TAG, TAG_GATE_MODE, DEFAULT_TAG_GATE_SAFETY


def validate_v3_alpha_tag_readiness() -> dict:
    """Validate final tag readiness. Does NOT execute git tag."""
    violations = []

    rc_gate = validate_v3_alpha_rc_gate()
    artifact_cs = validate_alpha_rc_artifact_consistency()

    if not rc_gate.get("pass", False):
        violations.append(f"RC gate failed: {len(rc_gate.get('violations', []))} violations")
    if not artifact_cs.get("pass", False):
        violations.append(f"artifact consistency failed: {len(artifact_cs.get('violations', []))} violations")

    # Safety checks
    for name, obj in [("rc_gate", rc_gate), ("artifact_consistency", artifact_cs)]:
        if obj.get("git_tag_execute_allowed") is True:
            violations.append(f"{name}.git_tag_execute_allowed must be False")
        if obj.get("git_push_tags_allowed") is True:
            violations.append(f"{name}.git_push_tags_allowed must be False")
        if obj.get("runtime_enabled") is True:
            violations.append(f"{name}.runtime_enabled must be False")
        if obj.get("real_trade_allowed") is True:
            violations.append(f"{name}.real_trade_allowed must be False")

    overall_status = "BLOCKED" if violations else "READY_FOR_TAG_REVIEW"

    return {
        "tag_gate_version": "V3_ALPHA_TAG_GATE_V10",
        "target_tag": TARGET_TAG,
        "mode": TAG_GATE_MODE,
        "overall_status": overall_status,
        "ready_for_tag_review": overall_status == "READY_FOR_TAG_REVIEW",
        "tag_command_preview": "git tag -a v3.0-alpha-rc1 -m 'Z-MATRIX-OS v3.0-alpha RC1'",
        "push_command_preview": "git push origin v3.0-alpha-rc1",
        "git_tag_execute_allowed": False,
        "git_push_tags_allowed": False,
        "rc_gate": rc_gate,
        "artifact_consistency": artifact_cs,
        "blocking_issues": violations,
        "safety": dict(DEFAULT_TAG_GATE_SAFETY),
        "real_trade_allowed": False,
        "broker_order_allowed": False,
        "runtime_enabled": False,
        "hermes_memory_write_allowed": False,
        "real_z9_write_allowed": False,
        "prompt_auto_injection_allowed": False,
        "system_prompt_write_allowed": False,
    }
