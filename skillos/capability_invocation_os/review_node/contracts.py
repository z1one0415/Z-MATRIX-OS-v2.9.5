"""Z9 Review Node contracts — validation without raising."""

from dataclasses import fields as dataclass_fields

from skillos.capability_invocation_os.research_report_node.models import Z9ReviewSnapshotCandidate
from skillos.capability_invocation_os.review_node.constants import (
    FORBIDDEN_INPUT_KEYS,
    FORBIDDEN_OUTPUT_KEYS,
    ALLOWED_REVIEW_SECTIONS,
    ALLOWED_REVIEW_LABELS,
)
from skillos.capability_invocation_os.review_node.models import (
    Z9ReviewDecision,
    Z9ReviewNodeRequest,
    Z9ReviewNodeResponse,
    Z9ReviewSection,
    Z9ReviewEvidence,
    Z2FeedbackCandidate,
)


def payload_contains_forbidden_inputs(payload) -> bool:
    """Recursively scan payload for any FORBIDDEN_INPUT_KEYS keys."""
    if isinstance(payload, dict):
        for key, value in payload.items():
            if key in FORBIDDEN_INPUT_KEYS:
                return True
            if payload_contains_forbidden_inputs(value):
                return True
    elif isinstance(payload, (list, tuple)):
        for item in payload:
            if payload_contains_forbidden_inputs(item):
                return True
    elif hasattr(payload, "__dataclass_fields__"):
        for f in dataclass_fields(payload):
            val = getattr(payload, f.name, None)
            if f.name in FORBIDDEN_INPUT_KEYS:
                return True
            if payload_contains_forbidden_inputs(val):
                return True
    return False


def payload_contains_forbidden_outputs(payload) -> bool:
    """Recursively scan payload for any FORBIDDEN_OUTPUT_KEYS keys."""
    if isinstance(payload, dict):
        for key, value in payload.items():
            if key in FORBIDDEN_OUTPUT_KEYS:
                return True
            if payload_contains_forbidden_outputs(value):
                return True
    elif isinstance(payload, (list, tuple)):
        for item in payload:
            if payload_contains_forbidden_outputs(item):
                return True
    elif hasattr(payload, "__dataclass_fields__"):
        for f in dataclass_fields(payload):
            val = getattr(payload, f.name, None)
            if f.name in FORBIDDEN_OUTPUT_KEYS:
                return True
            if payload_contains_forbidden_outputs(val):
                return True
    return False


def blocked_outputs_removed_complete(values) -> bool:
    """Check that FORBIDDEN_OUTPUT_KEYS is a subset of values."""
    return FORBIDDEN_OUTPUT_KEYS.issubset(set(values))


def validate_z9_review_request(request: Z9ReviewNodeRequest) -> Z9ReviewDecision:
    """Validate a Z9 review request. Never raises."""
    if not isinstance(request, Z9ReviewNodeRequest):
        return Z9ReviewDecision.DENY_Z9_SOURCE_FORBIDDEN
    if request.execution_requested:
        return Z9ReviewDecision.DENY_Z9_EXECUTION_FORBIDDEN
    if request.memory_mutation_requested:
        return Z9ReviewDecision.DENY_Z9_MEMORY_MUTATION_FORBIDDEN
    return Z9ReviewDecision.ALLOW_Z9_READONLY_REVIEW


def validate_z2_snapshot_candidate(candidate) -> Z9ReviewDecision:
    """Validate a Z2 Z9ReviewSnapshotCandidate. Never raises."""
    if not isinstance(candidate, Z9ReviewSnapshotCandidate):
        return Z9ReviewDecision.DENY_Z9_SOURCE_FORBIDDEN
    if not candidate.readonly_only:
        return Z9ReviewDecision.DENY_Z9_EXECUTION_FORBIDDEN
    if not candidate.no_trade_result:
        return Z9ReviewDecision.DENY_Z9_TRADE_RESULT_FORBIDDEN
    if not candidate.no_paper_trading:
        return Z9ReviewDecision.DENY_Z9_TRADE_RESULT_FORBIDDEN
    if not candidate.no_broker_action:
        return Z9ReviewDecision.DENY_Z9_TRADE_RESULT_FORBIDDEN
    if not candidate.no_position_change:
        return Z9ReviewDecision.DENY_Z9_TRADE_RESULT_FORBIDDEN
    # Check required hashes are non-empty (BLOCKER 3)
    if not all([
        candidate.report_node_id,
        candidate.source_graph_hash,
        candidate.evidence_chain_hash,
        candidate.research_summary_hash,
        candidate.risk_warning_hash,
    ]):
        return Z9ReviewDecision.DENY_Z9_EVIDENCE_INCOMPLETE
    # Check blocked_outputs_removed complete (BLOCKER 4 — empty list must fail)
    if not blocked_outputs_removed_complete(candidate.blocked_outputs_removed):
        return Z9ReviewDecision.DENY_Z9_OUTPUTS_UNSAFE
    # Check payload for forbidden inputs
    if payload_contains_forbidden_inputs(candidate):
        return Z9ReviewDecision.DENY_Z9_SOURCE_FORBIDDEN
    # Check payload for forbidden outputs
    if payload_contains_forbidden_outputs(candidate):
        return Z9ReviewDecision.DENY_Z9_OUTPUTS_UNSAFE
    return Z9ReviewDecision.ALLOW_Z9_READONLY_REVIEW


def validate_z9_review_section(section: Z9ReviewSection) -> Z9ReviewDecision:
    """Validate a Z9 review section. Never raises."""
    if not isinstance(section, Z9ReviewSection):
        return Z9ReviewDecision.DENY_Z9_SOURCE_FORBIDDEN
    if section.section_type not in ALLOWED_REVIEW_SECTIONS:
        return Z9ReviewDecision.DENY_Z9_SOURCE_FORBIDDEN
    if not section.readonly_only:
        return Z9ReviewDecision.DENY_Z9_EXECUTION_FORBIDDEN
    # Check blocked_outputs_removed complete (BLOCKER 4 — empty list must fail)
    if not blocked_outputs_removed_complete(section.blocked_outputs_removed):
        return Z9ReviewDecision.DENY_Z9_OUTPUTS_UNSAFE
    # Check payload for forbidden outputs
    if payload_contains_forbidden_outputs(section):
        return Z9ReviewDecision.DENY_Z9_OUTPUTS_UNSAFE
    return Z9ReviewDecision.ALLOW_Z9_READONLY_REVIEW


def validate_z9_review_response(response: Z9ReviewNodeResponse) -> Z9ReviewDecision:
    """Validate a full Z9 review response. Never raises."""
    if not isinstance(response, Z9ReviewNodeResponse):
        return Z9ReviewDecision.DENY_Z9_SOURCE_FORBIDDEN
    if not response.readonly_only:
        return Z9ReviewDecision.DENY_Z9_EXECUTION_FORBIDDEN
    if not response.no_trade_result:
        return Z9ReviewDecision.DENY_Z9_TRADE_RESULT_FORBIDDEN
    if not response.no_paper_trading:
        return Z9ReviewDecision.DENY_Z9_TRADE_RESULT_FORBIDDEN
    if not response.no_broker_action:
        return Z9ReviewDecision.DENY_Z9_TRADE_RESULT_FORBIDDEN
    if not response.no_position_change:
        return Z9ReviewDecision.DENY_Z9_TRADE_RESULT_FORBIDDEN
    if response.memory_mutation_enabled:
        return Z9ReviewDecision.DENY_Z9_MEMORY_MUTATION_FORBIDDEN
    # BLOCKER 4 — empty list must fail (same condition as below)
    if not blocked_outputs_removed_complete(response.forbidden_outputs_removed):
        return Z9ReviewDecision.DENY_Z9_OUTPUTS_UNSAFE
    # BLOCKER 5 — validate each section with validate_z9_review_section
    for section in response.sections:
        sec_decision = validate_z9_review_section(section)
        if sec_decision.value.startswith("DENY_"):
            return sec_decision
    # BLOCKER 5 — validate z2_feedback_candidate if present
    if response.z2_feedback_candidate is not None:
        fb_decision = validate_z2_feedback_candidate(response.z2_feedback_candidate)
        if fb_decision.value.startswith("DENY_"):
            return fb_decision
    # Scan evidence payload
    if payload_contains_forbidden_outputs(response.evidence):
        return Z9ReviewDecision.DENY_Z9_OUTPUTS_UNSAFE
    return Z9ReviewDecision.ALLOW_Z9_READONLY_REVIEW


def validate_z2_feedback_candidate(candidate: Z2FeedbackCandidate) -> Z9ReviewDecision:
    """Validate a Z2 feedback candidate. Never raises."""
    if not isinstance(candidate, Z2FeedbackCandidate):
        return Z9ReviewDecision.DENY_Z9_SOURCE_FORBIDDEN
    if not candidate.readonly_only:
        return Z9ReviewDecision.DENY_Z9_EXECUTION_FORBIDDEN
    if not candidate.requires_human_review:
        return Z9ReviewDecision.DENY_Z9_EXECUTION_FORBIDDEN
    # Review label must be in allowed set
    if candidate.review_label not in ALLOWED_REVIEW_LABELS:
        return Z9ReviewDecision.DENY_Z9_SOURCE_FORBIDDEN
    # Feedback candidates must not contain forbidden outputs
    if payload_contains_forbidden_outputs(candidate):
        return Z9ReviewDecision.DENY_Z9_OUTPUTS_UNSAFE
    return Z9ReviewDecision.ALLOW_Z9_READONLY_REVIEW
