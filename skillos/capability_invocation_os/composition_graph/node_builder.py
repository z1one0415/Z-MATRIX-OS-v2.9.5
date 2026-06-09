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
        node_type="a1_factor_bridge_response_node",
        payload=payload,
        hash_value=_hash(str(payload)),
        valid=True,
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
        node_type="a1_factor_bridge_denied_context_node",
        payload=payload,
        hash_value=_hash(str(payload)),
        valid=False,
    )


def build_factor_evidence_summary_node(evidence) -> CompositionGraphNode:
    """Build a factor evidence summary node."""
    node_id = f"node_evidence_{uuid.uuid4().hex[:8]}"
    payload = {"evidence": evidence}
    return CompositionGraphNode(
        node_id=node_id,
        node_type="factor_evidence_summary_node",
        payload=payload,
        hash_value=_hash(str(payload)),
        valid=True,
    )


def build_composition_summary_node(summary) -> CompositionGraphNode:
    """Build a composition summary node."""
    node_id = f"node_summary_{uuid.uuid4().hex[:8]}"
    payload = {"summary": summary}
    return CompositionGraphNode(
        node_id=node_id,
        node_type="composition_summary_node",
        payload=payload,
        hash_value=_hash(str(payload)),
        valid=True,
    )


def build_static_input_node(reason: str = "DISABLED_DEFAULT_P0") -> CompositionGraphNode:
    """Build a static input placeholder node (noop equivalent)."""
    node_id = f"node_static_{uuid.uuid4().hex[:8]}"
    return CompositionGraphNode(
        node_id=node_id,
        node_type="static_input_node",
        payload={"reason": reason},
        hash_value=_hash(reason),
        valid=True,
    )


# Legacy aliases for backwards compatibility
build_graph_evidence_node = build_factor_evidence_summary_node
build_graph_summary_node = build_composition_summary_node
build_graph_noop_node = build_static_input_node
