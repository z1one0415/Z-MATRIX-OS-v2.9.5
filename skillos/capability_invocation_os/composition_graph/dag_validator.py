"""Composition Graph DAG validation."""

from skillos.capability_invocation_os.composition_graph.constants import (
    ALLOWED_NODE_TYPES,
    BLOCKED_NODE_TYPES,
    ALLOWED_EDGE_TYPES,
    BLOCKED_EDGE_TYPES,
)
from skillos.capability_invocation_os.composition_graph.models import (
    CompositionGraphNode,
    CompositionGraphEdge,
)


def validate_dag_no_cycles(nodes: list[CompositionGraphNode], edges: list[CompositionGraphEdge]) -> bool:
    """Validate that the DAG has no cycles."""
    if not edges:
        return True
    adjacency: dict[str, list[str]] = {}
    for edge in edges:
        adjacency.setdefault(edge.source_node_id, []).append(edge.target_node_id)
    visited: set[str] = set()
    in_stack: set[str] = set()

    def _dfs(node_id: str) -> bool:
        if node_id in in_stack:
            return False
        if node_id in visited:
            return True
        visited.add(node_id)
        in_stack.add(node_id)
        for neighbor in adjacency.get(node_id, []):
            if not _dfs(neighbor):
                return False
        in_stack.discard(node_id)
        return True

    all_nodes = {n.node_id for n in nodes}
    for node_id in all_nodes:
        if node_id not in visited:
            if not _dfs(node_id):
                return False
    return True


def validate_dag_node_types(nodes: list[CompositionGraphNode]) -> bool:
    """Validate that all node types are allowed and none are blocked."""
    for node in nodes:
        if node.node_type in BLOCKED_NODE_TYPES:
            return False
        if node.node_type not in ALLOWED_NODE_TYPES:
            return False
    return True


def validate_dag_edge_types(edges: list[CompositionGraphEdge]) -> bool:
    """Validate that all edge types are allowed and none are blocked."""
    for edge in edges:
        if edge.edge_type in BLOCKED_EDGE_TYPES:
            return False
        if edge.edge_type not in ALLOWED_EDGE_TYPES:
            return False
    return True


def validate_dag_edge_connectivity(nodes: list[CompositionGraphNode], edges: list[CompositionGraphEdge]) -> bool:
    """Validate that all edges reference existing nodes."""
    node_ids = {n.node_id for n in nodes}
    for edge in edges:
        if edge.source_node_id not in node_ids:
            return False
        if edge.target_node_id not in node_ids:
            return False
    return True


def validate_denied_context_terminal(nodes: list[CompositionGraphNode], edges: list[CompositionGraphEdge]) -> bool:
    """Denied context nodes can only have outgoing edges to denied_context_edge/evidence_hash_edge/c1_handoff_edge/degradation_edge. They cannot feed composition_summary_node via any edge."""
    denied_node_ids = {n.node_id for n in nodes if n.node_type == "a1_factor_bridge_denied_context_node"}
    summary_node_ids = {n.node_id for n in nodes if n.node_type == "composition_summary_node"}
    allowed_outgoing = {"denied_context_edge", "evidence_hash_edge", "c1_handoff_edge", "degradation_edge"}

    for edge in edges:
        if edge.source_node_id in denied_node_ids:
            if edge.edge_type not in allowed_outgoing:
                return False
            if edge.target_node_id in summary_node_ids:
                return False
    return True


def validate_denied_context_cannot_feed_valid_summary(nodes: list[CompositionGraphNode], edges: list[CompositionGraphEdge]) -> bool:
    """Denied context node must never directly connect to composition_summary_node."""
    denied_ids = {n.node_id for n in nodes if n.node_type == "a1_factor_bridge_denied_context_node"}
    summary_ids = {n.node_id for n in nodes if n.node_type == "composition_summary_node"}
    for edge in edges:
        if edge.source_node_id in denied_ids and edge.target_node_id in summary_ids:
            return False
    return True


def validate_dag_integrity(nodes: list[CompositionGraphNode], edges: list[CompositionGraphEdge]) -> bool:
    """Run all DAG validations."""
    return (
        validate_dag_node_types(nodes)
        and validate_dag_edge_types(edges)
        and validate_dag_edge_connectivity(nodes, edges)
        and validate_dag_no_cycles(nodes, edges)
        and validate_denied_context_terminal(nodes, edges)
        and validate_denied_context_cannot_feed_valid_summary(nodes, edges)
    )
