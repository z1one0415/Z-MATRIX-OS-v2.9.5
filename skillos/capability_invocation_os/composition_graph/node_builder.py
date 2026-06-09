"""Composition Graph node builders."""

import hashlib
import uuid

from skillos.capability_invocation_os.composition_graph.models import (
    CompositionGraphNode,
    DeniedGraphContext,
)


def _hash(content: str) -> str:
    return hashlib.sha256(content.encode()).hexdigest()[:16]


def build_a1_bridge_response_node(response) -> CompositionGraphNode:
    """Build a graph node from an A1 bridge response."""
    node_id = f"node_bridge_{uuid.uuid4().hex[:8]}"
    payload = {
        "response_id": getattr(response, "response_id", ""),
        "decision": getattr(response, "decision", None),
        "mode": getattr(response, "mode", ""),
    }
    return CompositionGraphNode(
        node_id=node_id,
        node_type="a1_bridge_response",
        payload=payload,
        hash_value=_hash(str(payload)),
    )


def build_a1_bridge_denied_context_node(response, reason: str = "") -> CompositionGraphNode:
    """Build a denied context node from an A1 bridge denied response."""
    node_id = f"node_denied_{uuid.uuid4().hex[:8]}"
    decision_val = ""
    if hasattr(response, "decision") and response.decision is not None:
        decision_val = response.decision.value
    ctx = DeniedGraphContext(
        node_id=node_id,
        original_decision=decision_val,
        reason=reason,
    )
    payload = {
        "denied_context": ctx,
        "response_id": getattr(response, "response_id", ""),
    }
    return CompositionGraphNode(
        node_id=node_id,
        node_type="a1_bridge_denied_context",
        payload=payload,
        hash_value=_hash(str(payload)),
    )


def build_graph_evidence_node(evidence) -> CompositionGraphNode:
    """Build a graph evidence node."""
    node_id = f"node_evidence_{uuid.uuid4().hex[:8]}"
    payload = {"evidence": evidence}
    return CompositionGraphNode(
        node_id=node_id,
        node_type="graph_evidence",
        payload=payload,
        hash_value=_hash(str(payload)),
    )


def build_graph_noop_node() -> CompositionGraphNode:
    """Build a NOOP placeholder node."""
    node_id = f"node_noop_{uuid.uuid4().hex[:8]}"
    return CompositionGraphNode(
        node_id=node_id,
        node_type="graph_noop",
        payload={"reason": "DISABLED_DEFAULT_P0"},
        hash_value=_hash("noop"),
    )


def build_graph_summary_node(summary) -> CompositionGraphNode:
    """Build a graph source summary node."""
    node_id = f"node_summary_{uuid.uuid4().hex[:8]}"
    payload = {"summary": summary}
    return CompositionGraphNode(
        node_id=node_id,
        node_type="graph_source_summary",
        payload=payload,
        hash_value=_hash(str(payload)),
    )
