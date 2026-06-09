"""Composition Graph contract validation against A1 Factor Bridge responses."""

from skillos.capability_invocation_os.adapters.zmatrix_factor_bridge.models import (
    A1FactorBridgeResponse,
    A1FactorBridgeEvidence,
)
from skillos.capability_invocation_os.composition_graph.constants import (
    FORBIDDEN_GRAPH_OUTPUTS,
)
from skillos.capability_invocation_os.composition_graph.models import (
    CompositionGraphDecision,
)

_VALID_SOURCE_CLASSES = frozenset({
    "factor_library_fixture",
    "factor_library_disabled_default",
})


def validate_a1_bridge_response(response) -> CompositionGraphDecision:
    """Validate an A1 bridge response and return graph decision."""
    if not isinstance(response, A1FactorBridgeResponse):
        return CompositionGraphDecision.DENY_GRAPH_SOURCE_FORBIDDEN

    evidence = response.evidence
    if evidence is None:
        return CompositionGraphDecision.DENY_GRAPH_SOURCE_FORBIDDEN

    if isinstance(evidence, A1FactorBridgeEvidence):
        source_class = evidence.source_class
        no_real_source = evidence.no_real_source_flag
    elif isinstance(evidence, dict):
        source_class = evidence.get("source_class", "")
        no_real_source = evidence.get("no_real_source_flag", False)
    else:
        return CompositionGraphDecision.DENY_GRAPH_SOURCE_FORBIDDEN

    if source_class not in _VALID_SOURCE_CLASSES:
        return CompositionGraphDecision.DENY_GRAPH_SOURCE_FORBIDDEN

    if no_real_source is not True:
        return CompositionGraphDecision.DENY_GRAPH_REAL_SOURCE_FORBIDDEN

    removed = set(response.forbidden_outputs_removed)
    if not FORBIDDEN_GRAPH_OUTPUTS.issubset(removed):
        return CompositionGraphDecision.DENY_GRAPH_OUTPUTS_UNSAFE

    if response.decision.value.startswith("DENY_BRIDGE_"):
        return CompositionGraphDecision.DENY_GRAPH_BRIDGE_DENIED

    return CompositionGraphDecision.ALLOW_GRAPH_READONLY_SUMMARY


def validate_graph_node_type(node_type: str) -> bool:
    """Check if a node type is allowed."""
    from skillos.capability_invocation_os.composition_graph.constants import (
        ALLOWED_NODE_TYPES,
    )
    return node_type in ALLOWED_NODE_TYPES


def validate_graph_edge_type(edge_type: str) -> bool:
    """Check if an edge type is allowed."""
    from skillos.capability_invocation_os.composition_graph.constants import (
        ALLOWED_EDGE_TYPES,
    )
    return edge_type in ALLOWED_EDGE_TYPES


def validate_no_blocked_nodes(node_types: list[str]) -> bool:
    """Check that no blocked node types are present."""
    from skillos.capability_invocation_os.composition_graph.constants import (
        BLOCKED_NODE_TYPES,
    )
    return not any(nt in BLOCKED_NODE_TYPES for nt in node_types)


def validate_no_blocked_edges(edge_types: list[str]) -> bool:
    """Check that no blocked edge types are present."""
    from skillos.capability_invocation_os.composition_graph.constants import (
        BLOCKED_EDGE_TYPES,
    )
    return not any(et in BLOCKED_EDGE_TYPES for et in edge_types)
