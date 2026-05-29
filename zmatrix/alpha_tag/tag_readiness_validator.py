# allowlist: forbidden-token-definition
"""Tag Readiness Validator — aggregate RC gate + artifact consistency for final tag review"""
from __future__ import annotations

from zmatrix.alpha_rc.rc_gate_validator import validate_v3_alpha_rc_gate
from zmatrix.alpha_tag.artifact_consistency import validate_alpha_rc_artifact_consistency
from zmatrix.alpha_tag.schemas import TARGET_TAG, TAG_GATE_MODE, DEFAULT_TAG_GATE_SAFETY

_BLOCKED_FIELDS = [
    "real_trade_allowed", "broker_order_allowed", "auto_buy_allowed",
    "auto_sell_allowed", "auto_position_close_allowed", "real_z9_write_allowed",
    "hermes_memory_write_allowed", "auto_calibration_allowed",
    "prompt_auto_injection_allowed", "system_prompt_write_allowed",
    "runtime_injection_allowed", "runtime_enabled", "external_api_default_on",
    "git_tag_execute_allowed", "git_push_tags_allowed",
]


def _check_blocked_fields(prefix: str, record: dict) -> list[str]:
    """Check both top-level and safety nested blocked fields."""
    violations = []
    if not isinstance(record, dict):
        return violations
    for field in _BLOCKED_FIELDS:
        if record.get(field) is True:
            violations.append(f"{prefix}.{field} must be False")
    safety = record.get("safety", {})
    if safety is None:
        safety = {}
    if not isinstance(safety, dict):
        violations.append(f"{prefix}.safety must be dict")
        return violations
    for field in _BLOCKED_FIELDS:
        if safety.get(field) is True:
            violations.append(f"{prefix}.safety.{field} must be False")
    return violations


def validate_v3_alpha_tag_readiness() -> dict:
    """Validate final tag readiness. Does NOT execute git tag."""
    violations = []

    rc_gate = validate_v3_alpha_rc_gate()
    artifact_cs = validate_alpha_rc_artifact_consistency()

    if not rc_gate.get("pass", False):
        violations.append(f"RC gate failed: {len(rc_gate.get('violations', []))} violations")
    if not artifact_cs.get("pass", False):
        violations.append(f"artifact consistency failed: {len(artifact_cs.get('violations', []))} violations")

    # Recursive safety check
    candidate_output = {
        "safety": dict(DEFAULT_TAG_GATE_SAFETY),
        "git_tag_execute_allowed": False,
        "git_push_tags_allowed": False,
        "runtime_enabled": False,
        "real_trade_allowed": False,
        "broker_order_allowed": False,
        "hermes_memory_write_allowed": False,
        "real_z9_write_allowed": False,
        "prompt_auto_injection_allowed": False,
        "system_prompt_write_allowed": False,
    }

    for name, obj in {
        "rc_gate": rc_gate,
        "artifact_consistency": artifact_cs,
        "tag_readiness": candidate_output,
    }.items():
        violations.extend(_check_blocked_fields(name, obj))

    overall_status = "BLOCKED" if violations else "READY_FOR_TAG_REVIEW"

    return {
        "tag_gate_version": "V3_ALPHA_TAG_GATE_V10",
        "blocked_fields_checked": list(_BLOCKED_FIELDS),
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
