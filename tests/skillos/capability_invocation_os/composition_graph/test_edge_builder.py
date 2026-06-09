"""Tests for composition_graph.edge_builder."""

from skillos.capability_invocation_os.composition_graph.edge_builder import (
    build_bridge_to_graph_edge,
    build_graph_to_evidence_edge,
    build_graph_to_summary_edge,
    build_denied_to_context_edge,
    build_graph_to_noop_edge,
)
from skillos.capability_invocation_os.composition_graph.models import (
    CompositionGraphEdge,
)


def test_bridge_to_graph_edge_type():
    edge = build_bridge_to_graph_edge("src", "tgt")
    assert isinstance(edge, CompositionGraphEdge)
    assert edge.edge_type == "bridge_to_graph"


def test_bridge_to_graph_edge_connectivity():
    edge = build_bridge_to_graph_edge("node_a", "node_b")
    assert edge.source_node_id == "node_a"
    assert edge.target_node_id == "node_b"


def test_graph_to_evidence_edge():
    edge = build_graph_to_evidence_edge("src", "tgt")
    assert edge.edge_type == "graph_to_evidence"
    assert edge.edge_id.startswith("edge_g2e_")


def test_graph_to_summary_edge():
    edge = build_graph_to_summary_edge("src", "tgt")
    assert edge.edge_type == "graph_to_summary"
    assert edge.edge_id.startswith("edge_g2s_")


def test_denied_to_context_edge():
    edge = build_denied_to_context_edge("src", "tgt")
    assert edge.edge_type == "denied_to_context"
    assert edge.edge_id.startswith("edge_d2c_")


def test_graph_to_noop_edge():
    edge = build_graph_to_noop_edge("src", "tgt")
    assert edge.edge_type == "graph_to_noop"
    assert edge.edge_id.startswith("edge_g2n_")


def test_edge_has_hash():
    edge = build_bridge_to_graph_edge("a", "b")
    assert len(edge.hash_value) == 16
