"""Isolated runtime adapter for SkillOS Level 3.

Default disabled. Never blocks runtime. Never mutates result_envelope.
Never calls invoke_skill. Never warns caller. Enforcement always DISABLED.
"""

from copy import deepcopy
from typing import Any, Callable

from zmatrix.agent.skillos_level3_config import SkillOSLevel3Config, get_level3_config
from zmatrix.agent.skillos_level3_shadow_observer import observe_shadow_event


def build_runtime_adapter_event(
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
    """Build an adapter event dict with only allowed telemetry fields."""
    from zmatrix.agent.skillos_level3_shadow_observer import build_shadow_event
    return build_shadow_event(
        event_id=event_id, skill_id=skill_id, contract_id=contract_id,
        schema_validation_result=schema_validation_result,
        input_hash=input_hash, output_hash=output_hash,
        golden_match_status=golden_match_status,
        semantic_drift_status=semantic_drift_status,
        runtime_duration_bucket=runtime_duration_bucket,
        non_sensitive_error_category=non_sensitive_error_category,
    )


def run_level3_runtime_adapter(
    event: dict[str, Any],
    *,
    result_envelope: Any | None = None,
    config: SkillOSLevel3Config | None = None,
    observer_fn: Callable[[dict[str, Any], SkillOSLevel3Config | None], dict[str, Any]] = observe_shadow_event,
) -> dict[str, Any]:
    """Run Level 3 runtime adapter. Never blocks. Never mutates. Never warns.

    Args:
        event: shadow event dict from build_runtime_adapter_event.
        result_envelope: (unused, retained for future API compatibility)
        config: Level 3 config (default disabled if None)
        observer_fn: shadow observer to call (default: observe_shadow_event)

    Returns:
        dict with runtime_action, caller_visible_warning, result_envelope_mutation,
        runtime_blocking, enforcement, adapter_enabled, observer_called, written, error.
    """
    if config is None:
        config = get_level3_config()

    base = {
        "runtime_action": "CONTINUE",
        "caller_visible_warning": False,
        "result_envelope_mutation": False,
        "runtime_blocking": False,
        "enforcement": "DISABLED",
        "adapter_enabled": config.enabled,
        "observer_called": False,
        "written": False,
        "error": None,
    }

    if not config.enabled:
        return base

    # Enabled: call observer, catch all failures
    try:
        obs_result = observer_fn(event, config)
        base["observer_called"] = True
        base["written"] = obs_result.get("written", False)
    except Exception as e:
        base["error"] = str(e)
        # Observer failure must not block runtime
        base["runtime_action"] = "CONTINUE"
        base["observer_called"] = False

    return base
