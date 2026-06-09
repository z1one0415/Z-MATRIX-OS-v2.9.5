"""Tests for composition_graph.edge_builder."""
from skillos.capability_invocation_os.composition_graph.edge_builder import (
    build_a1_bridge_source_edge, build_evidence_hash_edge, build_degradation_edge,
    build_denied_context_edge, build_c1_handoff_edge, build_readonly_context_edge,
    build_bridge_to_graph_edge, build_graph_to_evidence_edge, build_graph_to_summary_edge,
    build_denied_to_context_edge, build_graph_to_noop_edge,
)
from skillos.capability_invocation_os.composition_graph.models import CompositionGraphEdge

def test_a1_bridge_source_edge_type():
    edge = build_a1_bridge_source_edge("src", "tgt")
    assert isinstance(edge, CompositionGraphEdge)
    assert edge.edge_type == "a1_bridge_source_edge"

def test_a1_bridge_source_edge_connectivity():
    edge = build_a1_bridge_source_edge("node_a", "node_b")
    assert edge.source_node_id == "node_a"
    assert edge.target_node_id == "node_b"

def test_evidence_hash_edge():
    edge = build_evidence_hash_edge("src", "tgt")
    assert edge.edge_type == "evidence_hash_edge"
    assert edge.edge_id.startswith("edge_evh_")

def test_degradation_edge():
    edge = build_degradation_edge("src", "tgt")
    assert edge.edge_type == "degradation_edge"
    assert edge.edge_id.startswith("edge_deg_")

def test_denied_context_edge():
    edge = build_denied_context_edge("src", "tgt")
    assert edge.edge_type == "denied_context_edge"
    assert edge.edge_id.startswith("edge_dnc_")

def test_c1_handoff_edge():
    edge = build_c1_handoff_edge("src", "tgt")
    assert edge.edge_type == "c1_handoff_edge"
    assert edge.edge_id.startswith("edge_c1h_")

def test_readonly_context_edge():
    edge = build_readonly_context_edge("src", "tgt")
    assert edge.edge_type == "readonly_context_edge"
    assert edge.edge_id.startswith("edge_roc_")

def test_edge_has_hash():
    assert len(build_a1_bridge_source_edge("a", "b").hash_value) == 16

def test_legacy_alias_bridge_to_graph():
    assert build_bridge_to_graph_edge("src", "tgt").edge_type == "a1_bridge_source_edge"

def test_legacy_alias_graph_to_evidence():
    assert build_graph_to_evidence_edge("src", "tgt").edge_type == "evidence_hash_edge"

def test_legacy_alias_graph_to_summary():
    assert build_graph_to_summary_edge("src", "tgt").edge_type == "degradation_edge"

def test_legacy_alias_denied_to_context():
    assert build_denied_to_context_edge("src", "tgt").edge_type == "denied_context_edge"

def test_legacy_alias_graph_to_noop():
    assert build_graph_to_noop_edge("src", "tgt").edge_type == "readonly_context_edge"

def test_canonical_names_in_allowed():
    from skillos.capability_invocation_os.composition_graph.constants import ALLOWED_EDGE_TYPES
    assert build_a1_bridge_source_edge("a", "b").edge_type in ALLOWED_EDGE_TYPES
    assert build_evidence_hash_edge("a", "b").edge_type in ALLOWED_EDGE_TYPES
    assert build_degradation_edge("a", "b").edge_type in ALLOWED_EDGE_TYPES
    assert build_denied_context_edge("a", "b").edge_type in ALLOWED_EDGE_TYPES
    assert build_c1_handoff_edge("a", "b").edge_type in ALLOWED_EDGE_TYPES
    assert build_readonly_context_edge("a", "b").edge_type in ALLOWED_EDGE_TYPES
