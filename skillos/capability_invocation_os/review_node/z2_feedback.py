"""Z9 Review Node Z2 feedback builder — advisory and readonly, no auto-patch."""

import uuid

from skillos.capability_invocation_os.review_node.models import (
    Z9ReviewDecision,
    Z9ReviewNodeResponse,
    Z2FeedbackCandidate,
)
from skillos.capability_invocation_os.review_node.constants import ALLOWED_REVIEW_LABELS


def build_z2_feedback_candidate(review_response=None) -> Z2FeedbackCandidate:
    """Build a Z2FeedbackCandidate from a Z9 review response.

    Feedback is advisory and readonly. No auto-patch or auto-update.
    """
    # Determine review label from evidence
    if review_response is None:
        return Z2FeedbackCandidate()
    review_label = "EXPLANATION_ACCEPTED_STRUCTURE_ONLY"
    evidence = review_response.evidence

    if evidence is None:
        return Z2FeedbackCandidate()
    
    if isinstance(evidence, dict):
        review_required = evidence.get("review_required", False)
        confidence_level = evidence.get("confidence_level", "LOW")
        missing_evidence = evidence.get("missing_evidence", [])
        degradation_status = evidence.get("degradation_status", "")
    elif hasattr(evidence, "review_required"):
        review_required = evidence.review_required
        confidence_level = getattr(evidence, "confidence_level", "LOW")
        missing_evidence = getattr(evidence, "missing_evidence", [])
        degradation_status = getattr(evidence, "degradation_status", "")
    else:
        review_required = False
        confidence_level = "LOW"
        missing_evidence = []
        degradation_status = ""

    # Build evidence gap summary
    evidence_gap_summary = ""
    if missing_evidence:
        evidence_gap_summary = f"Missing evidence: {', '.join(missing_evidence)}"

    # Build confidence alignment issue
    confidence_alignment_issue = ""
    if confidence_level == "LOW":
        confidence_alignment_issue = "Confidence is LOW; structural review only"
    elif review_required:
        confidence_alignment_issue = "Review required but confidence not fully assessed"

    # Build blocked output issue
    blocked_output_issue = ""
    if degradation_status == "degraded":
        blocked_output_issue = "Review response is degraded"

    # Determine review label
    if degradation_status == "degraded":
        review_label = "EXPLANATION_DEGRADED_EVIDENCE_GAP"
    elif missing_evidence:
        review_label = "EXPLANATION_REQUIRES_FUTURE_VALIDATION"
    elif confidence_level == "LOW":
        review_label = "EXPLANATION_CONFIDENCE_MISMATCH"
    elif review_required:
        review_label = "EXPLANATION_DEGRADED_EVIDENCE_GAP"
    else:
        review_label = "EXPLANATION_ACCEPTED_STRUCTURE_ONLY"

    # Default recommended revision
    recommended_report_revision = ""
    if missing_evidence:
        recommended_report_revision = f"Re-build report with complete evidence: {', '.join(missing_evidence)}"

    # Next validation requirement
    next_validation_requirement = "Re-validate after next research_report_node run with full data"

    if review_response is None:
        return Z2FeedbackCandidate()
    return Z2FeedbackCandidate(
        source_z2_report_node_id=getattr(review_response, "response_id", ""),
        review_label=review_label if review_label in ALLOWED_REVIEW_LABELS else "EXPLANATION_ACCEPTED_STRUCTURE_ONLY",
        evidence_gap_summary=evidence_gap_summary,
        confidence_alignment_issue=confidence_alignment_issue,
        blocked_output_issue=blocked_output_issue,
        missing_evidence=list(missing_evidence),
        recommended_report_revision=recommended_report_revision,
        next_validation_requirement=next_validation_requirement,
        readonly_only=True,
        requires_human_review=True,
    )


def validate_z2_feedback_candidate_fn(candidate: Z2FeedbackCandidate) -> Z9ReviewDecision:
    """Validate a Z2FeedbackCandidate. Never raises. Advisory/readonly only."""
    if not isinstance(candidate, Z2FeedbackCandidate):
        return Z9ReviewDecision.DENY_Z9_SOURCE_FORBIDDEN
    if not candidate.readonly_only:
        return Z9ReviewDecision.DENY_Z9_EXECUTION_FORBIDDEN
    if not candidate.requires_human_review:
        return Z9ReviewDecision.DENY_Z9_EXECUTION_FORBIDDEN
    if candidate.review_label not in ALLOWED_REVIEW_LABELS:
        return Z9ReviewDecision.DENY_Z9_SOURCE_FORBIDDEN
    return Z9ReviewDecision.ALLOW_Z9_READONLY_REVIEW
