from skillos.capability_invocation_os.adapters.zmatrix_factor_bridge.models import (
    A1FactorBridgeRequest,
    A1FactorBridgeDecision,
)
from skillos.capability_invocation_os.adapters.zmatrix_factor_bridge.constants import (
    ALLOWED_BRIDGE_INPUT_SOURCE_CLASSES,
    FORBIDDEN_BRIDGE_OUTPUTS,
)


def validate_bridge_request(request: A1FactorBridgeRequest) -> A1FactorBridgeDecision:
    if request.execution_requested:
        return A1FactorBridgeDecision.DENY_BRIDGE_EXECUTION_FORBIDDEN

    if request.source_class not in ALLOWED_BRIDGE_INPUT_SOURCE_CLASSES:
        return A1FactorBridgeDecision.DENY_BRIDGE_SOURCE_FORBIDDEN

    return A1FactorBridgeDecision.ALLOW_BRIDGE_READONLY_CONTEXT


def validate_factor_response_for_bridge(response) -> A1FactorBridgeDecision:
    """Validate a FactorInvocationResponse from the factor_library adapter.

    Checks safety FIRST (source/output/no-real-source), then factor denial.
    Preserves each denial semantic independently.
    Never raises. Never fail-closed.
    """
    # 1. Evidence existence check
    if response.evidence is None:
        return A1FactorBridgeDecision.DENY_BRIDGE_REAL_SOURCE_FORBIDDEN

    # 2. Source class check
    source_class = getattr(response.evidence, "source_class", "")
    if source_class not in ALLOWED_BRIDGE_INPUT_SOURCE_CLASSES:
        return A1FactorBridgeDecision.DENY_BRIDGE_SOURCE_FORBIDDEN

    # 3. No real source check
    if hasattr(response.evidence, "no_real_source_flag"):
        if response.evidence.no_real_source_flag is not True:
            return A1FactorBridgeDecision.DENY_BRIDGE_REAL_SOURCE_FORBIDDEN

    # 4. Forbidden outputs removed existence check
    if not hasattr(response, "forbidden_outputs_removed"):
        return A1FactorBridgeDecision.DENY_BRIDGE_OUTPUTS_UNSAFE

    # 5. Forbidden outputs coverage check
    removed = set(response.forbidden_outputs_removed)
    if not FORBIDDEN_BRIDGE_OUTPUTS.issubset(removed):
        return A1FactorBridgeDecision.DENY_BRIDGE_OUTPUTS_UNSAFE

    # 6. Payload safety check (no forbidden fields present)
    for field in FORBIDDEN_BRIDGE_OUTPUTS:
        if hasattr(response, field):
            val = getattr(response, field, None)
            if val is not None and val != False and val != []:
                return A1FactorBridgeDecision.DENY_BRIDGE_OUTPUTS_UNSAFE

    # 7. Factor-level denial check (only after source/output/no-real-source all pass)
    if response.decision.value.startswith("DENY_"):
        return A1FactorBridgeDecision.DENY_BRIDGE_FACTOR_DENIED

    return A1FactorBridgeDecision.ALLOW_BRIDGE_READONLY_CONTEXT


def validate_no_forbidden_outputs(payload: dict) -> A1FactorBridgeDecision:
    """Check that no forbidden outputs exist in the payload."""
    for k in payload:
        if k in FORBIDDEN_BRIDGE_OUTPUTS:
            return A1FactorBridgeDecision.DENY_BRIDGE_OUTPUTS_UNSAFE
    return A1FactorBridgeDecision.ALLOW_BRIDGE_READONLY_CONTEXT


def validate_no_real_source(response) -> A1FactorBridgeDecision:
    """Check that the response has no_real_source_flag set."""
    if response.evidence is not None:
        if hasattr(response.evidence, "no_real_source_flag"):
            if response.evidence.no_real_source_flag is True:
                return A1FactorBridgeDecision.ALLOW_BRIDGE_READONLY_CONTEXT
    return A1FactorBridgeDecision.DENY_BRIDGE_REAL_SOURCE_FORBIDDEN
