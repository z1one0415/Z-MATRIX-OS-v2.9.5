"""Tests for composition_graph.dag_validator."""

from skillos.capability_invocation_os.composition_graph.dag_validator import (
    validate_dag_no_cycles,
    validate_dag_node_types,
    validate_dag_edge_types,
    validate_dag_edge_connectivity,
    validate_dag_integrity,
)
from skillos.capability_invocation_os.composition_graph.models import (
    CompositionGraphNode,
    CompositionGraphEdge,
)


def test_no_cycles_empty():
    assert validate_dag_no_cycles([], []) is True


def test_no_cycles_linear():
    nodes = [
        CompositionGraphNode(node_id="a", node_type="graph_noop"),
        CompositionGraphNode(node_id="b", node_type="graph_noop"),
    ]
    edges = [
        CompositionGraphEdge(edge_id="e1", edge_type="graph_to_noop", source_node_id="a", target_node_id="b"),
    ]
    assert validate_dag_no_cycles(nodes, edges) is True


def test_cycles_detected():
    nodes = [
        CompositionGraphNode(node_id="a", node_type="graph_noop"),
        CompositionGraphNode(node_id="b", node_type="graph_noop"),
    ]
    edges = [
        CompositionGraphEdge(edge_id="e1", edge_type="graph_to_noop", source_node_id="a", target_node_id="b"),
        CompositionGraphEdge(edge_id="e2", edge_type="graph_to_noop", source_node_id="b", target_node_id="a"),
    ]
    assert validate_dag_no_cycles(nodes, edges) is False


def test_node_types_valid():
    nodes = [
        CompositionGraphNode(node_id="a", node_type="a1_bridge_response"),
        CompositionGraphNode(node_id="b", node_type="graph_evidence"),
    ]
    assert validate_dag_node_types(nodes) is True


def test_node_types_blocked():
    nodes = [
        CompositionGraphNode(node_id="a", node_type="execution_node"),
    ]
    assert validate_dag_node_types(nodes) is False


def test_edge_types_valid():
    edges = [
        CompositionGraphEdge(edge_id="e1", edge_type="bridge_to_graph", source_node_id="a", target_node_id="b"),
    ]
    assert validate_dag_edge_types(edges) is True


def test_edge_types_blocked():
    edges = [
        CompositionGraphEdge(edge_id="e1", edge_type="execution_edge", source_node_id="a", target_node_id="b"),
    ]
    assert validate_dag_edge_types(edges) is False


def test_edge_connectivity_valid():
    nodes = [
        CompositionGraphNode(node_id="a", node_type="graph_noop"),
        CompositionGraphNode(node_id="b", node_type="graph_noop"),
    ]
    edges = [
        CompositionGraphEdge(edge_id="e1", edge_type="graph_to_noop", source_node_id="a", target_node_id="b"),
    ]
    assert validate_dag_edge_connectivity(nodes, edges) is True


def test_edge_connectivity_invalid():
    nodes = [
        CompositionGraphNode(node_id="a", node_type="graph_noop"),
    ]
    edges = [
        CompositionGraphEdge(edge_id="e1", edge_type="graph_to_noop", source_node_id="a", target_node_id="missing"),
    ]
    assert validate_dag_edge_connectivity(nodes, edges) is False


def test_integrity_pass():
    nodes = [
        CompositionGraphNode(node_id="a", node_type="a1_bridge_response"),
        CompositionGraphNode(node_id="b", node_type="graph_evidence"),
    ]
    edges = [
        CompositionGraphEdge(edge_id="e1", edge_type="bridge_to_graph", source_node_id="a", target_node_id="b"),
    ]
    assert validate_dag_integrity(nodes, edges) is True


def test_integrity_fail_blocked_node():
    nodes = [
        CompositionGraphNode(node_id="a", node_type="execution_node"),
    ]
    edges = []
    assert validate_dag_integrity(nodes, edges) is False
