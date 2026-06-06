"""Isolated shadow observer for SkillOS Level 3.

Default disabled. Never blocks runtime. Never mutates result_envelope.
Never calls invoke_skill. Never warns caller.
"""

from typing import Any

from zmatrix.agent.skillos_level3_config import SkillOSLevel3Config, get_level3_config
from zmatrix.agent.skillos_level3_audit_writer import write_shadow_audit_event


def build_shadow_event(
    *,
    event_id: str,
    skill_id: str,
    contract_id: str | None = None,
    schema_validation_result: str | None = None,
    input_hash: str | None = None,
    output_hash: str | None = None,
    golden_match_status: str | None = None,
    semantic_drift_status: str | None = None,
    runtime_duration_bucket: str | None = None,
    non_sensitive_error_category: str | None = None,
) -> dict[str, Any]:
    """Build a shadow event dict with only allowed telemetry fields."""
    event: dict[str, Any] = {
        "event_id": event_id,
        "skill_id": skill_id,
        "created_by": "skillos_level3_shadow_observer",
    }
    if contract_id:
        event["contract_id"] = contract_id
    if schema_validation_result:
        event["schema_validation_result"] = schema_validation_result
    if input_hash:
        event["input_hash"] = input_hash
    if output_hash:
        event["output_hash"] = output_hash
    if golden_match_status:
        event["golden_match_status"] = golden_match_status
    if semantic_drift_status:
        event["semantic_drift_status"] = semantic_drift_status
    if runtime_duration_bucket:
        event["runtime_duration_bucket"] = runtime_duration_bucket
    if non_sensitive_error_category:
        event["non_sensitive_error_category"] = non_sensitive_error_category
    return event


def observe_shadow_event(
    event: dict[str, Any],
    config: SkillOSLevel3Config | None = None,
) -> dict[str, Any]:
    """Observe shadow event. Never blocks. Never warns. Enforcement always DISABLED."""
    if config is None:
        config = get_level3_config()

    result = {
        "runtime_action": "CONTINUE",
        "caller_visible_warning": False,
        "result_envelope_mutation": False,
        "runtime_blocking": False,
        "enforcement": "DISABLED",
        "written": False,
    }

    if not config.enabled:
        return result

    write_result = write_shadow_audit_event(event, config)
    result["written"] = write_result.get("written", False)
    # Writer failure must not affect runtime
    return result
