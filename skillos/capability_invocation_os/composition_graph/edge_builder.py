"""Composition Graph edge builders."""

import hashlib
import uuid

from skillos.capability_invocation_os.composition_graph.models import (
    CompositionGraphEdge,
)


def _hash(content: str) -> str:
    return hashlib.sha256(content.encode()).hexdigest()[:16]


def build_bridge_to_graph_edge(source_node_id: str, target_node_id: str) -> CompositionGraphEdge:
    """Build a bridge_to_graph edge."""
    edge_id = f"edge_b2g_{uuid.uuid4().hex[:8]}"
    return CompositionGraphEdge(
        edge_id=edge_id,
        edge_type="bridge_to_graph",
        source_node_id=source_node_id,
        target_node_id=target_node_id,
        hash_value=_hash(f"{source_node_id}->{target_node_id}"),
    )


def build_graph_to_evidence_edge(source_node_id: str, target_node_id: str) -> CompositionGraphEdge:
    """Build a graph_to_evidence edge."""
    edge_id = f"edge_g2e_{uuid.uuid4().hex[:8]}"
    return CompositionGraphEdge(
        edge_id=edge_id,
        edge_type="graph_to_evidence",
        source_node_id=source_node_id,
        target_node_id=target_node_id,
        hash_value=_hash(f"{source_node_id}->{target_node_id}"),
    )


def build_graph_to_summary_edge(source_node_id: str, target_node_id: str) -> CompositionGraphEdge:
    """Build a graph_to_summary edge."""
    edge_id = f"edge_g2s_{uuid.uuid4().hex[:8]}"
    return CompositionGraphEdge(
        edge_id=edge_id,
        edge_type="graph_to_summary",
        source_node_id=source_node_id,
        target_node_id=target_node_id,
        hash_value=_hash(f"{source_node_id}->{target_node_id}"),
    )


def build_denied_to_context_edge(source_node_id: str, target_node_id: str) -> CompositionGraphEdge:
    """Build a denied_to_context edge."""
    edge_id = f"edge_d2c_{uuid.uuid4().hex[:8]}"
    return CompositionGraphEdge(
        edge_id=edge_id,
        edge_type="denied_to_context",
        source_node_id=source_node_id,
        target_node_id=target_node_id,
        hash_value=_hash(f"{source_node_id}->{target_node_id}"),
    )


def build_graph_to_noop_edge(source_node_id: str, target_node_id: str) -> CompositionGraphEdge:
    """Build a graph_to_noop edge."""
    edge_id = f"edge_g2n_{uuid.uuid4().hex[:8]}"
    return CompositionGraphEdge(
        edge_id=edge_id,
        edge_type="graph_to_noop",
        source_node_id=source_node_id,
        target_node_id=target_node_id,
        hash_value=_hash(f"{source_node_id}->{target_node_id}"),
    )
