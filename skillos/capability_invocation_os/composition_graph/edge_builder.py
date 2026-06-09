"""Composition Graph edge builders."""

import hashlib
import uuid

from skillos.capability_invocation_os.composition_graph.models import (
    CompositionGraphEdge,
)


def _hash(content: str) -> str:
    return hashlib.sha256(content.encode()).hexdigest()[:16]


def build_a1_bridge_source_edge(source_node_id: str, target_node_id: str) -> CompositionGraphEdge:
    """Build an a1_bridge_source_edge."""
    edge_id = f"edge_a1b_{uuid.uuid4().hex[:8]}"
    return CompositionGraphEdge(
        edge_id=edge_id,
        edge_type="a1_bridge_source_edge",
        source_node_id=source_node_id,
        target_node_id=target_node_id,
        hash_value=_hash(f"{source_node_id}->{target_node_id}"),
    )


def build_evidence_hash_edge(source_node_id: str, target_node_id: str) -> CompositionGraphEdge:
    """Build an evidence_hash_edge."""
    edge_id = f"edge_evh_{uuid.uuid4().hex[:8]}"
    return CompositionGraphEdge(
        edge_id=edge_id,
        edge_type="evidence_hash_edge",
        source_node_id=source_node_id,
        target_node_id=target_node_id,
        hash_value=_hash(f"{source_node_id}->{target_node_id}"),
    )


def build_degradation_edge(source_node_id: str, target_node_id: str) -> CompositionGraphEdge:
    """Build a degradation_edge."""
    edge_id = f"edge_deg_{uuid.uuid4().hex[:8]}"
    return CompositionGraphEdge(
        edge_id=edge_id,
        edge_type="degradation_edge",
        source_node_id=source_node_id,
        target_node_id=target_node_id,
        hash_value=_hash(f"{source_node_id}->{target_node_id}"),
    )


def build_denied_context_edge(source_node_id: str, target_node_id: str) -> CompositionGraphEdge:
    """Build a denied_context_edge."""
    edge_id = f"edge_dnc_{uuid.uuid4().hex[:8]}"
    return CompositionGraphEdge(
        edge_id=edge_id,
        edge_type="denied_context_edge",
        source_node_id=source_node_id,
        target_node_id=target_node_id,
        hash_value=_hash(f"{source_node_id}->{target_node_id}"),
    )


def build_c1_handoff_edge(source_node_id: str, target_node_id: str) -> CompositionGraphEdge:
    """Build a c1_handoff_edge."""
    edge_id = f"edge_c1h_{uuid.uuid4().hex[:8]}"
    return CompositionGraphEdge(
        edge_id=edge_id,
        edge_type="c1_handoff_edge",
        source_node_id=source_node_id,
        target_node_id=target_node_id,
        hash_value=_hash(f"{source_node_id}->{target_node_id}"),
    )


def build_readonly_context_edge(source_node_id: str, target_node_id: str) -> CompositionGraphEdge:
    """Build a readonly_context_edge."""
    edge_id = f"edge_roc_{uuid.uuid4().hex[:8]}"
    return CompositionGraphEdge(
        edge_id=edge_id,
        edge_type="readonly_context_edge",
        source_node_id=source_node_id,
        target_node_id=target_node_id,
        hash_value=_hash(f"{source_node_id}->{target_node_id}"),
    )


# Legacy aliases for backwards compat
build_bridge_to_graph_edge = build_a1_bridge_source_edge
build_graph_to_evidence_edge = build_evidence_hash_edge
build_graph_to_summary_edge = build_degradation_edge
build_denied_to_context_edge = build_denied_context_edge
build_graph_to_noop_edge = build_readonly_context_edge
