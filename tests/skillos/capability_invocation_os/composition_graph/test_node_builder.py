"""Tests for composition_graph.node_builder."""

from skillos.capability_invocation_os.adapters.zmatrix_factor_bridge.models import (
    A1FactorBridgeResponse,
    A1FactorBridgeDecision,
    A1FactorBridgeEvidence,
)
from skillos.capability_invocation_os.composition_graph.constants import FORBIDDEN_GRAPH_OUTPUTS
from skillos.capability_invocation_os.composition_graph.node_builder import (
    build_a1_bridge_response_node,
    build_a1_bridge_denied_context_node,
    build_graph_evidence_node,
    build_graph_noop_node,
    build_graph_summary_node,
)
from skillos.capability_invocation_os.composition_graph.models import (
    CompositionGraphNode,
    CompositionGraphEvidence,
    GraphSourceSummary,
)


def _make_response():
    return A1FactorBridgeResponse(
        response_id="test-node",
        decision=A1FactorBridgeDecision.ALLOW_BRIDGE_READONLY_CONTEXT,
        evidence=A1FactorBridgeEvidence(
            source_commit="P1_FIXTURE_ONLY",
            source_class="factor_library_fixture",
            no_real_source_flag=True,
            fixture_source_commit="P1_FIXTURE_ONLY",
            request_hash="r",
            response_hash_placeholder="r",
            factor_decision_hash="f",
            bridge_decision_hash="b",
            permission_tier="T0",
            forbidden_outputs_removed_hash="h",
            rollback_marker=False,
            privacy_marker=True,
            c1_handoff_marker=True,
        ),
        forbidden_outputs_removed=sorted(FORBIDDEN_GRAPH_OUTPUTS),
        degraded=False,
        mode="DISABLED_DEFAULT_P0",
        bridge_enabled=False,
        runtime_enabled=False,
        adapter_execution_enabled=False,
        capability_execution_enabled=False,
    )


def test_build_bridge_response_node_type():
    node = build_a1_bridge_response_node(_make_response())
    assert isinstance(node, CompositionGraphNode)
    assert node.node_type == "a1_bridge_response"


def test_build_bridge_response_node_has_id():
    node = build_a1_bridge_response_node(_make_response())
    assert node.node_id.startswith("node_bridge_")


def test_build_bridge_response_node_has_hash():
    node = build_a1_bridge_response_node(_make_response())
    assert len(node.hash_value) == 16


def test_build_denied_context_node():
    node = build_a1_bridge_denied_context_node(_make_response(), reason="test_reason")
    assert node.node_type == "a1_bridge_denied_context"
    assert node.node_id.startswith("node_denied_")


def test_build_evidence_node():
    ev = CompositionGraphEvidence()
    node = build_graph_evidence_node(ev)
    assert node.node_type == "graph_evidence"
    assert node.node_id.startswith("node_evidence_")


def test_build_noop_node():
    node = build_graph_noop_node()
    assert node.node_type == "graph_noop"
    assert node.node_id.startswith("node_noop_")


def test_build_summary_node():
    summary = GraphSourceSummary(source_class="test", total_nodes=1)
    node = build_graph_summary_node(summary)
    assert node.node_type == "graph_source_summary"
    assert node.node_id.startswith("node_summary_")
