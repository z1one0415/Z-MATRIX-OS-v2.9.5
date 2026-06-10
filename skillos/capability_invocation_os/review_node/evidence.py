"""Z9 Review Node evidence building — hash-based, no I/O."""

import hashlib
import json

from skillos.capability_invocation_os.research_report_node.models import Z9ReviewSnapshotCandidate
from skillos.capability_invocation_os.review_node.constants import FORBIDDEN_OUTPUT_KEYS
from skillos.capability_invocation_os.review_node.models import Z9ReviewEvidence


def _stable_hash(data: str) -> str:
    """Produce a stable SHA-256 hex digest."""
    return hashlib.sha256(data.encode("utf-8")).hexdigest()


def build_z9_review_node_hash(response_id: str, mode: str) -> str:
    """Build a hash for the Z9 review node itself."""
    payload = json.dumps({"response_id": response_id, "mode": mode}, sort_keys=True)
    return _stable_hash(payload)


def build_z9_review_section_hash(section_id: str, section_type: str) -> str:
    """Build a hash for a Z9 review section."""
    payload = json.dumps({"section_id": section_id, "section_type": section_type}, sort_keys=True)
    return _stable_hash(payload)


def build_z9_feedback_candidate_hash(feedback_id: str, review_label: str) -> str:
    """Build a hash for a Z2 feedback candidate."""
    payload = json.dumps({"feedback_id": feedback_id, "review_label": review_label}, sort_keys=True)
    return _stable_hash(payload)


def build_z9_review_evidence_from_z2_snapshot(
    snapshot: Z9ReviewSnapshotCandidate,
    response_id: str = "",
) -> Z9ReviewEvidence:
    """Build Z9ReviewEvidence from a Z2 Z9ReviewSnapshotCandidate."""
    node_hash = build_z9_review_node_hash(response_id, "DISABLED_DEFAULT_P0")

    evidence = Z9ReviewEvidence(
        source_z2_report_node_id=snapshot.report_node_id,
        source_graph_hash=snapshot.source_graph_hash,
        factor_context_summary_hash=snapshot.factor_context_summary_hash,
        evidence_chain_hash=snapshot.evidence_chain_hash,
        research_summary_hash=snapshot.research_summary_hash,
        risk_warning_hash=snapshot.risk_warning_hash,
        confidence_level=snapshot.confidence_level,
        confidence_reason=snapshot.confidence_reason,
        missing_evidence=list(snapshot.missing_evidence),
        degradation_status=snapshot.degradation_status,
        blocked_outputs_removed=list(snapshot.blocked_outputs_removed),
        review_required=snapshot.review_required,
        review_reason=snapshot.review_reason,
        readonly_only=True,
        z9_review_node_hash=node_hash,
        z9_review_section_hash="",
        z9_feedback_candidate_hash="",
        rollback_marker=False,
        privacy_marker=True,
    )

    return evidence
