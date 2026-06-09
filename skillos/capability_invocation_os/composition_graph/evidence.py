"""Composition Graph evidence builders."""

import hashlib

from skillos.capability_invocation_os.adapters.zmatrix_factor_bridge.models import (
    A1FactorBridgeResponse,
    A1FactorBridgeEvidence,
)
from skillos.capability_invocation_os.composition_graph.models import (
    CompositionGraphEvidence,
)


def _sha256(content: str) -> str:
    return hashlib.sha256(content.encode()).hexdigest()[:16]


def build_graph_node_hash(node_id: str, node_type: str, payload: str = "") -> str:
    """Build a deterministic hash for a graph node."""
    return _sha256(f"node:{node_id}:{node_type}:{payload}")


def build_graph_edge_hash(edge_id: str, edge_type: str, source: str, target: str) -> str:
    """Build a deterministic hash for a graph edge."""
    return _sha256(f"edge:{edge_id}:{edge_type}:{source}->{target}")


def build_graph_evidence_from_a1_response(response: A1FactorBridgeResponse) -> CompositionGraphEvidence:
    """Build graph evidence from an A1 bridge response."""
    evidence = response.evidence
    if isinstance(evidence, A1FactorBridgeEvidence):
        source_commit = evidence.source_commit
        source_class = evidence.source_class
        no_real_source_flag = evidence.no_real_source_flag
        fixture_source_commit = evidence.fixture_source_commit
        permission_tier = evidence.permission_tier
        forbidden_hash = evidence.forbidden_outputs_removed_hash
        rollback_marker = evidence.rollback_marker
        privacy_marker = evidence.privacy_marker
        c1_handoff_marker = evidence.c1_handoff_marker
        a1_evidence_hash = _sha256(str(evidence))
    elif isinstance(evidence, dict):
        source_commit = evidence.get("source_commit", "")
        source_class = evidence.get("source_class", "")
        no_real_source_flag = evidence.get("no_real_source_flag", True)
        fixture_source_commit = evidence.get("fixture_source_commit", "")
        permission_tier = evidence.get("permission_tier", "T0")
        forbidden_hash = evidence.get("forbidden_outputs_removed_hash", "")
        rollback_marker = evidence.get("rollback_marker", False)
        privacy_marker = evidence.get("privacy_marker", True)
        c1_handoff_marker = evidence.get("c1_handoff_marker", True)
        a1_evidence_hash = _sha256(str(evidence))
    else:
        return CompositionGraphEvidence()

    return CompositionGraphEvidence(
        source_commit=source_commit,
        source_class=source_class,
        no_real_source_flag=no_real_source_flag,
        fixture_source_commit=fixture_source_commit,
        graph_node_hash="",
        graph_edge_hash="",
        a1_evidence_hash=a1_evidence_hash,
        permission_tier=permission_tier,
        forbidden_outputs_removed_hash=forbidden_hash,
        rollback_marker=rollback_marker,
        privacy_marker=privacy_marker,
        c1_handoff_marker=c1_handoff_marker,
    )


def build_graph_c1_handoff(evidence: CompositionGraphEvidence) -> dict:
    """Build a C1 handoff marker from graph evidence."""
    return {
        "c1_handoff_marker": evidence.c1_handoff_marker,
        "source_class": evidence.source_class,
        "permission_tier": evidence.permission_tier,
        "graph_node_hash": evidence.graph_node_hash,
        "graph_edge_hash": evidence.graph_edge_hash,
        "a1_evidence_hash": evidence.a1_evidence_hash,
    }
