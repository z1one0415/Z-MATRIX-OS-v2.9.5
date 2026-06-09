"""Composition Graph Factor Bridge — main orchestrator class."""

import uuid

from skillos.capability_invocation_os.composition_graph.kill_switch import (
    should_force_disabled,
)
from skillos.capability_invocation_os.composition_graph.config import (
    is_composition_graph_enabled,
)
from skillos.capability_invocation_os.composition_graph.contracts import (
    validate_a1_bridge_response,
)
from skillos.capability_invocation_os.composition_graph.dag_validator import (
    validate_dag_integrity,
)
from skillos.capability_invocation_os.composition_graph.models import (
    CompositionGraphDecision,
    CompositionGraphResponse,
)
from skillos.capability_invocation_os.composition_graph.degradation import (
    build_disabled_default_response,
    build_denied_source_response,
    build_denied_real_source_response,
    build_denied_outputs_unsafe_response,
    build_denied_bridge_response,
    build_denied_dag_invalid_response,
    build_allowed_readonly_response,
)
from skillos.capability_invocation_os.composition_graph.node_builder import (
    build_a1_bridge_response_node,
    build_a1_bridge_denied_context_node,
    build_factor_evidence_summary_node,
    build_static_input_node,
)
from skillos.capability_invocation_os.composition_graph.edge_builder import (
    build_a1_bridge_source_edge,
    build_evidence_hash_edge,
    build_readonly_context_edge,
)
from skillos.capability_invocation_os.composition_graph.evidence import (
    build_graph_evidence_from_a1_response,
)
from skillos.capability_invocation_os.composition_graph.constants import GRAPH_MODE


class CompositionGraphFactorBridge:
    """Main composition graph bridge — P0 disabled default."""

    def __init__(self, fixture_mode: bool = False):
        self._fixture_mode = fixture_mode

    def _should_build_graph(self, a1_bridge_response=None) -> bool:
        """Determine if the graph should be built."""
        if should_force_disabled():
            return False
        if not is_composition_graph_enabled():
            return False
        if not self._fixture_mode:
            return False
        if a1_bridge_response is None:
            return False
        return True

    def process(self, a1_bridge_response=None) -> CompositionGraphResponse:
        """Process an A1 bridge response through the composition graph."""
        response_id = f"graph_{uuid.uuid4().hex[:12]}"

        if not self._should_build_graph(a1_bridge_response):
            return build_disabled_default_response(response_id=response_id)

        decision = validate_a1_bridge_response(a1_bridge_response)

        if decision == CompositionGraphDecision.DENY_GRAPH_SOURCE_FORBIDDEN:
            return build_denied_source_response(
                response_id=response_id, reason="source_validation_failed"
            )

        if decision == CompositionGraphDecision.DENY_GRAPH_REAL_SOURCE_FORBIDDEN:
            return build_denied_real_source_response(response_id=response_id)

        if decision == CompositionGraphDecision.DENY_GRAPH_OUTPUTS_UNSAFE:
            return build_denied_outputs_unsafe_response(response_id=response_id)

        if decision == CompositionGraphDecision.DENY_GRAPH_BRIDGE_DENIED:
            return build_denied_bridge_response(response_id=response_id)

        # ALLOW path — build readonly graph
        bridge_node = build_a1_bridge_response_node(a1_bridge_response)
        graph_evidence = build_graph_evidence_from_a1_response(a1_bridge_response)
        evidence_node = build_factor_evidence_summary_node(graph_evidence)

        edge = build_a1_bridge_source_edge(bridge_node.node_id, evidence_node.node_id)
        evidence_edge = build_evidence_hash_edge(
            bridge_node.node_id, evidence_node.node_id
        )

        nodes = [bridge_node, evidence_node]
        edges = [edge, evidence_edge]

        # Validate DAG integrity before returning allowed graph
        if not validate_dag_integrity(nodes, edges):
            return build_denied_dag_invalid_response(response_id=response_id)

        return build_allowed_readonly_response(
            response_id=response_id,
            nodes=nodes,
            edges=edges,
            evidence=graph_evidence,
        )
