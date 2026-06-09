"""Tests for composition_graph.models."""

from skillos.capability_invocation_os.composition_graph.models import (
    CompositionGraphDecision,
    CompositionGraphResponse,
    CompositionGraphNode,
    CompositionGraphEdge,
    CompositionGraphEvidence,
    DeniedGraphContext,
    GraphSourceSummary,
)


def test_decision_enum_has_allow():
    assert CompositionGraphDecision.ALLOW_GRAPH_READONLY_SUMMARY.value == "ALLOW_GRAPH_READONLY_SUMMARY"


def test_decision_enum_has_6_deny():
    deny_values = [d for d in CompositionGraphDecision if d.value.startswith("DENY_GRAPH_")]
    assert len(deny_values) == 6


def test_decision_enum_has_disabled_noop():
    assert CompositionGraphDecision.DISABLED_DEFAULT_NOOP.value == "DISABLED_DEFAULT_NOOP"


def test_decision_enum_total_count():
    assert len(CompositionGraphDecision) == 8


def test_response_defaults():
    r = CompositionGraphResponse()
    assert r.response_id == ""
    assert r.decision == CompositionGraphDecision.DISABLED_DEFAULT_NOOP
    assert r.degraded is True
    assert r.mode == "DISABLED_DEFAULT_P0"
    assert r.graph_enabled is False
    assert r.execution_enabled is False


def test_node_defaults():
    n = CompositionGraphNode()
    assert n.node_id == ""
    assert n.node_type == "graph_noop"
    assert n.payload == {}
    assert n.hash_value == ""


def test_edge_defaults():
    e = CompositionGraphEdge()
    assert e.edge_id == ""
    assert e.edge_type == "graph_to_noop"
    assert e.source_node_id == ""
    assert e.target_node_id == ""


def test_evidence_defaults():
    ev = CompositionGraphEvidence()
    assert ev.source_class == "factor_library_fixture"
    assert ev.no_real_source_flag is True
    assert ev.permission_tier == "T0"
    assert ev.privacy_marker is True
    assert ev.c1_handoff_marker is True


def test_denied_context_defaults():
    dc = DeniedGraphContext()
    assert dc.node_id == ""
    assert dc.original_decision == ""
    assert dc.reason == ""


def test_source_summary_defaults():
    ss = GraphSourceSummary()
    assert ss.source_class == ""
    assert ss.total_nodes == 0
    assert ss.total_edges == 0
    assert ss.allowed == 0
    assert ss.denied == 0
