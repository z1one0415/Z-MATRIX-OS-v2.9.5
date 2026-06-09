"""Research Report Node evidence building — hash-based, no I/O."""

import hashlib
import json

from skillos.capability_invocation_os.composition_graph.models import (
    CompositionGraphResponse,
    CompositionGraphEvidence,
)
from skillos.capability_invocation_os.research_report_node.constants import (
    FORBIDDEN_REPORT_OUTPUTS,
)
from skillos.capability_invocation_os.research_report_node.models import (
    ResearchReportEvidence,
)


def _stable_hash(data: str) -> str:
    """Produce a stable SHA-256 hex digest."""
    return hashlib.sha256(data.encode("utf-8")).hexdigest()


def build_z2_report_node_hash(response_id: str, mode: str) -> str:
    """Build a hash for the report node itself."""
    payload = json.dumps({"response_id": response_id, "mode": mode}, sort_keys=True)
    return _stable_hash(payload)


def build_z2_report_section_hash(section_id: str, section_type: str) -> str:
    """Build a hash for a report section."""
    payload = json.dumps({"section_id": section_id, "section_type": section_type}, sort_keys=True)
    return _stable_hash(payload)


def build_z2_report_evidence_hash(evidence: ResearchReportEvidence) -> str:
    """Build a hash for report evidence."""
    payload = json.dumps({
        "source_class": evidence.source_class,
        "no_real_source_flag": evidence.no_real_source_flag,
        "fixture_source_commit": evidence.fixture_source_commit,
        "permission_tier": evidence.permission_tier,
    }, sort_keys=True)
    return _stable_hash(payload)


def build_report_evidence_refs(sections: list) -> list:
    """Build evidence reference hashes from sections."""
    refs = []
    for section in sections:
        h = build_z2_report_section_hash(
            getattr(section, "section_id", ""),
            getattr(section, "section_type", ""),
        )
        refs.append(h)
    return refs


def build_report_evidence_from_b1_graph(
    b1_response: CompositionGraphResponse,
    response_id: str = "",
) -> ResearchReportEvidence:
    """Build ResearchReportEvidence from B1 CompositionGraphResponse."""
    b1_evidence = b1_response.evidence

    # Extract fields from B1 evidence (may be dict or dataclass)
    if isinstance(b1_evidence, CompositionGraphEvidence):
        source_class = b1_evidence.source_class
        no_real_source_flag = b1_evidence.no_real_source_flag
        fixture_source_commit = b1_evidence.fixture_source_commit
        graph_node_hash = b1_evidence.graph_node_hash
        graph_edge_hash = b1_evidence.graph_edge_hash
        permission_tier = b1_evidence.permission_tier
        forbidden_outputs_removed_hash = b1_evidence.forbidden_outputs_removed_hash
        rollback_marker = b1_evidence.rollback_marker
        privacy_marker = b1_evidence.privacy_marker
        c1_handoff_marker = b1_evidence.c1_handoff_marker
    elif isinstance(b1_evidence, dict):
        source_class = b1_evidence.get("source_class", "")
        no_real_source_flag = b1_evidence.get("no_real_source_flag", True)
        fixture_source_commit = b1_evidence.get("fixture_source_commit", "")
        graph_node_hash = b1_evidence.get("graph_node_hash", "")
        graph_edge_hash = b1_evidence.get("graph_edge_hash", "")
        permission_tier = b1_evidence.get("permission_tier", "T0")
        forbidden_outputs_removed_hash = b1_evidence.get("forbidden_outputs_removed_hash", "")
        rollback_marker = b1_evidence.get("rollback_marker", False)
        privacy_marker = b1_evidence.get("privacy_marker", True)
        c1_handoff_marker = b1_evidence.get("c1_handoff_marker", True)
    else:
        source_class = ""
        no_real_source_flag = True
        fixture_source_commit = ""
        graph_node_hash = ""
        graph_edge_hash = ""
        permission_tier = "T0"
        forbidden_outputs_removed_hash = ""
        rollback_marker = False
        privacy_marker = True
        c1_handoff_marker = True

    node_hash = build_z2_report_node_hash(response_id, "DISABLED_DEFAULT_P0")
    forbidden_hash = _stable_hash(json.dumps(sorted(FORBIDDEN_REPORT_OUTPUTS)))

    evidence = ResearchReportEvidence(
        source_class=source_class,
        no_real_source_flag=no_real_source_flag,
        fixture_source_commit=fixture_source_commit,
        request_hash="",
        response_hash_placeholder="",
        factor_decision_hash="",
        bridge_decision_hash="",
        graph_node_hash=graph_node_hash,
        graph_edge_hash=graph_edge_hash,
        permission_tier=permission_tier,
        forbidden_outputs_removed_hash=forbidden_hash,
        rollback_marker=rollback_marker,
        privacy_marker=privacy_marker,
        c1_handoff_marker=c1_handoff_marker,
        z2_report_node_hash=node_hash,
        z2_report_section_hash="",
        z2_report_evidence_hash="",
    )

    evidence_hash = build_z2_report_evidence_hash(evidence)
    # Since frozen, we need to reconstruct with the hash
    evidence = ResearchReportEvidence(
        source_class=evidence.source_class,
        no_real_source_flag=evidence.no_real_source_flag,
        fixture_source_commit=evidence.fixture_source_commit,
        request_hash=evidence.request_hash,
        response_hash_placeholder=evidence.response_hash_placeholder,
        factor_decision_hash=evidence.factor_decision_hash,
        bridge_decision_hash=evidence.bridge_decision_hash,
        graph_node_hash=evidence.graph_node_hash,
        graph_edge_hash=evidence.graph_edge_hash,
        permission_tier=evidence.permission_tier,
        forbidden_outputs_removed_hash=evidence.forbidden_outputs_removed_hash,
        rollback_marker=evidence.rollback_marker,
        privacy_marker=evidence.privacy_marker,
        c1_handoff_marker=evidence.c1_handoff_marker,
        z2_report_node_hash=evidence.z2_report_node_hash,
        z2_report_section_hash=evidence.z2_report_section_hash,
        z2_report_evidence_hash=evidence_hash,
    )

    return evidence
