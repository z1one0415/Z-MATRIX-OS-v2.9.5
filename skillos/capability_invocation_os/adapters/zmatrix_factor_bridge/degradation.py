import uuid

from skillos.capability_invocation_os.adapters.zmatrix_factor_bridge.models import (
    A1FactorBridgeResponse,
    A1FactorBridgeDecision,
)
from skillos.capability_invocation_os.adapters.zmatrix_factor_bridge.constants import (
    FORBIDDEN_BRIDGE_OUTPUTS,
)


def allow_bridge_readonly_context() -> A1FactorBridgeResponse:
    return A1FactorBridgeResponse(
        response_id=str(uuid.uuid4()),
        decision=A1FactorBridgeDecision.ALLOW_BRIDGE_READONLY_CONTEXT,
        degraded=False,
    )


def allow_bridge_evidence_summary() -> A1FactorBridgeResponse:
    return A1FactorBridgeResponse(
        response_id=str(uuid.uuid4()),
        decision=A1FactorBridgeDecision.ALLOW_BRIDGE_EVIDENCE_SUMMARY,
        degraded=False,
    )


def deny_bridge_source_forbidden() -> A1FactorBridgeResponse:
    return A1FactorBridgeResponse(
        response_id=str(uuid.uuid4()),
        decision=A1FactorBridgeDecision.DENY_BRIDGE_SOURCE_FORBIDDEN,
        degraded=True,
    )


def deny_bridge_real_source_forbidden() -> A1FactorBridgeResponse:
    return A1FactorBridgeResponse(
        response_id=str(uuid.uuid4()),
        decision=A1FactorBridgeDecision.DENY_BRIDGE_REAL_SOURCE_FORBIDDEN,
        degraded=True,
    )


def deny_bridge_outputs_unsafe() -> A1FactorBridgeResponse:
    return A1FactorBridgeResponse(
        response_id=str(uuid.uuid4()),
        decision=A1FactorBridgeDecision.DENY_BRIDGE_OUTPUTS_UNSAFE,
        degraded=True,
    )


def deny_bridge_execution_forbidden() -> A1FactorBridgeResponse:
    return A1FactorBridgeResponse(
        response_id=str(uuid.uuid4()),
        decision=A1FactorBridgeDecision.DENY_BRIDGE_EXECUTION_FORBIDDEN,
        degraded=True,
    )


def deny_bridge_factor_denied() -> A1FactorBridgeResponse:
    return A1FactorBridgeResponse(
        response_id=str(uuid.uuid4()),
        decision=A1FactorBridgeDecision.DENY_BRIDGE_FACTOR_DENIED,
        degraded=True,
    )


def disabled_default_noop() -> A1FactorBridgeResponse:
    return A1FactorBridgeResponse(
        response_id=str(uuid.uuid4()),
        decision=A1FactorBridgeDecision.DISABLED_DEFAULT_NOOP,
        degraded=True,
    )
