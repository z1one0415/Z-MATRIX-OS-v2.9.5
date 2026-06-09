"""Tests for composition_graph.dag_validator."""
from skillos.capability_invocation_os.composition_graph.dag_validator import (
    validate_dag_no_cycles, validate_dag_node_types, validate_dag_edge_types,
    validate_dag_edge_connectivity, validate_dag_integrity,
    validate_denied_context_terminal, validate_denied_context_cannot_feed_valid_summary,
)
from skillos.capability_invocation_os.composition_graph.models import CompositionGraphNode, CompositionGraphEdge

def test_no_cycles_empty():
    assert validate_dag_no_cycles([], []) is True

def test_no_cycles_linear():
    nodes = [CompositionGraphNode(node_id="a", node_type="static_input_node"), CompositionGraphNode(node_id="b", node_type="static_input_node")]
    edges = [CompositionGraphEdge(edge_id="e1", edge_type="readonly_context_edge", source_node_id="a", target_node_id="b")]
    assert validate_dag_no_cycles(nodes, edges) is True

def test_cycles_detected():
    nodes = [CompositionGraphNode(node_id="a", node_type="static_input_node"), CompositionGraphNode(node_id="b", node_type="static_input_node")]
    edges = [CompositionGraphEdge(edge_id="e1", edge_type="readonly_context_edge", source_node_id="a", target_node_id="b"), CompositionGraphEdge(edge_id="e2", edge_type="readonly_context_edge", source_node_id="b", target_node_id="a")]
    assert validate_dag_no_cycles(nodes, edges) is False

def test_node_types_valid():
    nodes = [CompositionGraphNode(node_id="a", node_type="a1_factor_bridge_response_node"), CompositionGraphNode(node_id="b", node_type="factor_evidence_summary_node")]
    assert validate_dag_node_types(nodes) is True

def test_node_types_blocked():
    assert validate_dag_node_types([CompositionGraphNode(node_id="a", node_type="factor_library_direct_node")]) is False

def test_edge_types_valid():
    assert validate_dag_edge_types([CompositionGraphEdge(edge_id="e1", edge_type="a1_bridge_source_edge", source_node_id="a", target_node_id="b")]) is True

def test_edge_types_blocked():
    assert validate_dag_edge_types([CompositionGraphEdge(edge_id="e1", edge_type="execution_edge", source_node_id="a", target_node_id="b")]) is False

def test_edge_connectivity_valid():
    nodes = [CompositionGraphNode(node_id="a", node_type="static_input_node"), CompositionGraphNode(node_id="b", node_type="static_input_node")]
    edges = [CompositionGraphEdge(edge_id="e1", edge_type="readonly_context_edge", source_node_id="a", target_node_id="b")]
    assert validate_dag_edge_connectivity(nodes, edges) is True

def test_edge_connectivity_invalid():
    nodes = [CompositionGraphNode(node_id="a", node_type="static_input_node")]
    edges = [CompositionGraphEdge(edge_id="e1", edge_type="readonly_context_edge", source_node_id="a", target_node_id="missing")]
    assert validate_dag_edge_connectivity(nodes, edges) is False

def test_integrity_pass():
    nodes = [CompositionGraphNode(node_id="a", node_type="a1_factor_bridge_response_node"), CompositionGraphNode(node_id="b", node_type="factor_evidence_summary_node")]
    edges = [CompositionGraphEdge(edge_id="e1", edge_type="a1_bridge_source_edge", source_node_id="a", target_node_id="b")]
    assert validate_dag_integrity(nodes, edges) is True

def test_integrity_fail_blocked_node():
    assert validate_dag_integrity([CompositionGraphNode(node_id="a", node_type="factor_library_direct_node")], []) is False

def test_denied_context_terminal_accepted():
    nodes = [CompositionGraphNode(node_id="d1", node_type="a1_factor_bridge_denied_context_node"), CompositionGraphNode(node_id="e1", node_type="factor_evidence_summary_node")]
    edges = [CompositionGraphEdge(edge_id="e1", edge_type="denied_context_edge", source_node_id="d1", target_node_id="e1")]
    assert validate_denied_context_terminal(nodes, edges) is True

def test_denied_context_feeding_summary_denied():
    nodes = [CompositionGraphNode(node_id="d1", node_type="a1_factor_bridge_denied_context_node"), CompositionGraphNode(node_id="s1", node_type="composition_summary_node")]
    edges = [CompositionGraphEdge(edge_id="e1", edge_type="denied_context_edge", source_node_id="d1", target_node_id="s1")]
    assert validate_denied_context_terminal(nodes, edges) is False

def test_denied_context_via_readonly_edge_denied():
    nodes = [CompositionGraphNode(node_id="d1", node_type="a1_factor_bridge_denied_context_node"), CompositionGraphNode(node_id="o1", node_type="factor_evidence_summary_node")]
    edges = [CompositionGraphEdge(edge_id="e1", edge_type="readonly_context_edge", source_node_id="d1", target_node_id="o1")]
    assert validate_denied_context_terminal(nodes, edges) is False

def test_denied_cannot_feed_summary_pass():
    nodes = [CompositionGraphNode(node_id="d1", node_type="a1_factor_bridge_denied_context_node"), CompositionGraphNode(node_id="e1", node_type="factor_evidence_summary_node"), CompositionGraphNode(node_id="s1", node_type="composition_summary_node")]
    edges = [CompositionGraphEdge(edge_id="e1", edge_type="denied_context_edge", source_node_id="d1", target_node_id="e1")]
    assert validate_denied_context_cannot_feed_valid_summary(nodes, edges) is True

def test_denied_cannot_feed_summary_fail():
    nodes = [CompositionGraphNode(node_id="d1", node_type="a1_factor_bridge_denied_context_node"), CompositionGraphNode(node_id="s1", node_type="composition_summary_node")]
    edges = [CompositionGraphEdge(edge_id="e1", edge_type="evidence_hash_edge", source_node_id="d1", target_node_id="s1")]
    assert validate_denied_context_cannot_feed_valid_summary(nodes, edges) is False

def test_integrity_fails_on_denied_feeding_summary():
    nodes = [CompositionGraphNode(node_id="d1", node_type="a1_factor_bridge_denied_context_node"), CompositionGraphNode(node_id="s1", node_type="composition_summary_node")]
    edges = [CompositionGraphEdge(edge_id="e1", edge_type="denied_context_edge", source_node_id="d1", target_node_id="s1")]
    assert validate_dag_integrity(nodes, edges) is False

def test_denied_with_evidence_hash_edge_ok():
    nodes = [CompositionGraphNode(node_id="d1", node_type="a1_factor_bridge_denied_context_node"), CompositionGraphNode(node_id="e1", node_type="factor_evidence_summary_node")]
    edges = [CompositionGraphEdge(edge_id="e1", edge_type="evidence_hash_edge", source_node_id="d1", target_node_id="e1")]
    assert validate_denied_context_terminal(nodes, edges) is True

def test_denied_with_c1_handoff_edge_ok():
    nodes = [CompositionGraphNode(node_id="d1", node_type="a1_factor_bridge_denied_context_node"), CompositionGraphNode(node_id="c1", node_type="capability_registry_node")]
    edges = [CompositionGraphEdge(edge_id="e1", edge_type="c1_handoff_edge", source_node_id="d1", target_node_id="c1")]
    assert validate_denied_context_terminal(nodes, edges) is True
