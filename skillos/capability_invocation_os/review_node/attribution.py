"""Z9 Review Node attribution — explanation attribution only, no profit attribution."""

from skillos.capability_invocation_os.research_report_node.models import Z9ReviewSnapshotCandidate
from skillos.capability_invocation_os.review_node.models import Z9ReviewEvidence
from skillos.capability_invocation_os.review_node.constants import ALLOWED_REVIEW_LABELS


def build_explanation_attribution(
    snapshot: Z9ReviewSnapshotCandidate,
    evidence: Z9ReviewEvidence,
) -> dict:
    """Build explanation attribution from snapshot and evidence. Readonly, no profit attribution.

    Returns a dict with only explanation attribution types, never profit/alpha/PnL.
    """
    attribution = {"attribution_type": "EXPLANATION_ONLY", "readonly_only": True}

    if evidence is None:
        attribution["no_evidence"] = True
        return attribution

    # Base attribution from review flags
    if evidence is not None:
        attribution["review_required"] = evidence.review_required
    else:
        attribution["review_required"] = False
    if evidence is not None and evidence.review_reason:
        attribution["review_reason"] = evidence.review_reason

    # Evidence chain reflection
    hashes_present = []
    hashes_missing = []
    if evidence is not None and evidence.source_graph_hash:
        hashes_present.append("source_graph_hash")
    else:
        hashes_missing.append("source_graph_hash")
    if evidence is not None and evidence.evidence_chain_hash:
        hashes_present.append("evidence_chain_hash")
    else:
        hashes_missing.append("evidence_chain_hash")
    if evidence is not None and evidence.factor_context_summary_hash:
        hashes_present.append("factor_context_summary_hash")
    else:
        hashes_missing.append("factor_context_summary_hash")
    if evidence is not None and evidence.research_summary_hash:
        hashes_present.append("research_summary_hash")
    else:
        hashes_missing.append("research_summary_hash")
    if evidence is not None and evidence.risk_warning_hash:
        hashes_present.append("risk_warning_hash")
    else:
        hashes_missing.append("risk_warning_hash")

    attribution["evidence_hashes_present"] = hashes_present
    attribution["evidence_hashes_missing"] = hashes_missing

    # Confidence attribution
    if evidence is not None:
        attribution["confidence_level"] = evidence.confidence_level
    else:
        attribution["confidence_level"] = "LOW"
    attribution["confidence_reason"] = evidence.confidence_reason

    # Missing evidence attribution
    attribution["missing_evidence"] = list(evidence.missing_evidence if evidence is not None else None)

    # Degradation attribution
    attribution["degradation_status"] = evidence.degradation_status

    # Determine best-fit review label
    review_label = ""
    if evidence is not None and not evidence.review_required and evidence.confidence_level == "LOW":
        review_label = "EXPLANATION_ACCEPTED_STRUCTURE_ONLY"
    elif hashes_missing:
        review_label = "EXPLANATION_DEGRADED_EVIDENCE_GAP"
    elif evidence is not None and evidence.blocked_outputs_removed if evidence is not None else None:
        review_label = "EXPLANATION_BLOCKED_OUTPUT_RISK"
    elif evidence is not None and evidence.confidence_level == "LOW":
        review_label = "EXPLANATION_CONFIDENCE_MISMATCH"
    else:
        review_label = "EXPLANATION_ACCEPTED_STRUCTURE_ONLY"

    if review_label in ALLOWED_REVIEW_LABELS:
        attribution["review_label"] = review_label

    return attribution
