"""Tests for composition_graph.models."""
from skillos.capability_invocation_os.composition_graph.models import (
    CompositionGraphDecision, CompositionGraphNode, CompositionGraphEdge,
    CompositionGraphEvidence, DeniedGraphContext, GraphSourceSummary, CompositionGraphResponse,
)

def test_decision_enum_values():
    assert CompositionGraphDecision.ALLOW_GRAPH_READONLY_SUMMARY.value == "ALLOW_GRAPH_READONLY_SUMMARY"
    assert CompositionGraphDecision.DENY_GRAPH_DAG_INVALID.value == "DENY_GRAPH_DAG_INVALID"

def test_decision_enum_count():
    assert len(CompositionGraphDecision) == 9

def test_node_defaults():
    node = CompositionGraphNode()
    assert node.node_type == "static_input_node"
    assert node.valid is True

def test_edge_defaults():
    assert CompositionGraphEdge().edge_type == "readonly_context_edge"

def test_evidence_defaults():
    ev = CompositionGraphEvidence()
    assert ev.no_real_source_flag is True
    assert ev.source_class == "factor_library_fixture"

def test_denied_context_defaults():
    ctx = DeniedGraphContext()
    assert ctx.node_id == ""
    assert ctx.reason == ""

def test_graph_source_summary():
    s = GraphSourceSummary(source_class="test", total_nodes=5, total_edges=3, allowed=4, denied=1)
    assert s.total_nodes == 5
    assert s.denied == 1

def test_response_defaults():
    resp = CompositionGraphResponse()
    assert resp.decision == CompositionGraphDecision.DISABLED_DEFAULT_NOOP
    assert resp.degraded is True
    assert resp.execution_enabled is False
