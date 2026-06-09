"""Composition Graph degradation builders — P0 disabled defaults."""

from skillos.capability_invocation_os.composition_graph.models import (
    CompositionGraphResponse,
    CompositionGraphDecision,
)
from skillos.capability_invocation_os.composition_graph.constants import (
    FORBIDDEN_GRAPH_OUTPUTS,
    GRAPH_MODE,
)


def build_disabled_default_response(response_id: str = "") -> CompositionGraphResponse:
    """Build a DISABLED_DEFAULT_NOOP response."""
    return CompositionGraphResponse(
        response_id=response_id,
        decision=CompositionGraphDecision.DISABLED_DEFAULT_NOOP,
        nodes=[],
        edges=[],
        evidence={},
        forbidden_outputs_removed=sorted(FORBIDDEN_GRAPH_OUTPUTS),
        degraded=True,
        mode=GRAPH_MODE,
        graph_enabled=False,
        execution_enabled=False,
    )


def build_denied_source_response(response_id: str = "", reason: str = "") -> CompositionGraphResponse:
    """Build a DENY_GRAPH_SOURCE_FORBIDDEN response."""
    return CompositionGraphResponse(
        response_id=response_id,
        decision=CompositionGraphDecision.DENY_GRAPH_SOURCE_FORBIDDEN,
        nodes=[],
        edges=[],
        evidence={"reason": reason},
        forbidden_outputs_removed=sorted(FORBIDDEN_GRAPH_OUTPUTS),
        degraded=True,
        mode=GRAPH_MODE,
        graph_enabled=False,
        execution_enabled=False,
    )


def build_denied_real_source_response(response_id: str = "") -> CompositionGraphResponse:
    """Build a DENY_GRAPH_REAL_SOURCE_FORBIDDEN response."""
    return CompositionGraphResponse(
        response_id=response_id,
        decision=CompositionGraphDecision.DENY_GRAPH_REAL_SOURCE_FORBIDDEN,
        nodes=[],
        edges=[],
        evidence={},
        forbidden_outputs_removed=sorted(FORBIDDEN_GRAPH_OUTPUTS),
        degraded=True,
        mode=GRAPH_MODE,
        graph_enabled=False,
        execution_enabled=False,
    )


def build_denied_outputs_unsafe_response(response_id: str = "") -> CompositionGraphResponse:
    """Build a DENY_GRAPH_OUTPUTS_UNSAFE response."""
    return CompositionGraphResponse(
        response_id=response_id,
        decision=CompositionGraphDecision.DENY_GRAPH_OUTPUTS_UNSAFE,
        nodes=[],
        edges=[],
        evidence={},
        forbidden_outputs_removed=sorted(FORBIDDEN_GRAPH_OUTPUTS),
        degraded=True,
        mode=GRAPH_MODE,
        graph_enabled=False,
        execution_enabled=False,
    )


def build_denied_bridge_response(response_id: str = "") -> CompositionGraphResponse:
    """Build a DENY_GRAPH_BRIDGE_DENIED response."""
    return CompositionGraphResponse(
        response_id=response_id,
        decision=CompositionGraphDecision.DENY_GRAPH_BRIDGE_DENIED,
        nodes=[],
        edges=[],
        evidence={},
        forbidden_outputs_removed=sorted(FORBIDDEN_GRAPH_OUTPUTS),
        degraded=True,
        mode=GRAPH_MODE,
        graph_enabled=False,
        execution_enabled=False,
    )


def build_denied_execution_response(response_id: str = "") -> CompositionGraphResponse:
    """Build a DENY_GRAPH_EXECUTION_FORBIDDEN response."""
    return CompositionGraphResponse(
        response_id=response_id,
        decision=CompositionGraphDecision.DENY_GRAPH_EXECUTION_FORBIDDEN,
        nodes=[],
        edges=[],
        evidence={},
        forbidden_outputs_removed=sorted(FORBIDDEN_GRAPH_OUTPUTS),
        degraded=True,
        mode=GRAPH_MODE,
        graph_enabled=False,
        execution_enabled=False,
    )


def build_denied_factor_response(response_id: str = "") -> CompositionGraphResponse:
    """Build a DENY_GRAPH_FACTOR_DENIED response."""
    return CompositionGraphResponse(
        response_id=response_id,
        decision=CompositionGraphDecision.DENY_GRAPH_FACTOR_DENIED,
        nodes=[],
        edges=[],
        evidence={},
        forbidden_outputs_removed=sorted(FORBIDDEN_GRAPH_OUTPUTS),
        degraded=True,
        mode=GRAPH_MODE,
        graph_enabled=False,
        execution_enabled=False,
    )


def build_allowed_readonly_response(
    response_id: str = "",
    nodes: list | None = None,
    edges: list | None = None,
    evidence=None,
) -> CompositionGraphResponse:
    """Build an ALLOW_GRAPH_READONLY_SUMMARY response."""
    return CompositionGraphResponse(
        response_id=response_id,
        decision=CompositionGraphDecision.ALLOW_GRAPH_READONLY_SUMMARY,
        nodes=nodes or [],
        edges=edges or [],
        evidence=evidence or {},
        forbidden_outputs_removed=sorted(FORBIDDEN_GRAPH_OUTPUTS),
        degraded=False,
        mode=GRAPH_MODE,
        graph_enabled=False,
        execution_enabled=False,
    )
