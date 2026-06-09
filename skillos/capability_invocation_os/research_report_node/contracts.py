"""Research Report Node contracts — validation without raising."""

from dataclasses import fields as dataclass_fields

from skillos.capability_invocation_os.composition_graph.models import (
    CompositionGraphResponse,
)
from skillos.capability_invocation_os.research_report_node.constants import (
    FORBIDDEN_REPORT_OUTPUTS,
    ALLOWED_REPORT_SECTIONS,
    ALLOWED_CONFIDENCE_LEVELS,
)
from skillos.capability_invocation_os.research_report_node.models import (
    ResearchReportDecision,
    ResearchReportNodeRequest,
    ResearchReportNodeResponse,
    ResearchReportSection,
    ResearchReportEvidence,
    Z9ReviewSnapshotCandidate,
)


def payload_contains_forbidden_outputs(payload) -> bool:
    """Recursively scan payload for any FORBIDDEN_REPORT_OUTPUTS keys."""
    if isinstance(payload, dict):
        for key, value in payload.items():
            if key in FORBIDDEN_REPORT_OUTPUTS:
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
            if f.name in FORBIDDEN_REPORT_OUTPUTS:
                return True
            if payload_contains_forbidden_outputs(val):
                return True
    return False


def validate_report_request(request: ResearchReportNodeRequest) -> ResearchReportDecision:
    """Validate a report request. Never raises."""
    if not isinstance(request, ResearchReportNodeRequest):
        return ResearchReportDecision.DENY_Z2_SOURCE_FORBIDDEN
    if request.execution_requested:
        return ResearchReportDecision.DENY_Z2_EXECUTION_FORBIDDEN
    return ResearchReportDecision.ALLOW_Z2_READONLY_REPORT


def validate_b1_graph_response_for_report(
    b1_response,
) -> ResearchReportDecision:
    """Validate B1 CompositionGraphResponse for report generation. Never raises."""
    if not isinstance(b1_response, CompositionGraphResponse):
        return ResearchReportDecision.DENY_Z2_SOURCE_FORBIDDEN

    # Check evidence no_real_source_flag
    evidence = b1_response.evidence
    if hasattr(evidence, "no_real_source_flag"):
        if evidence.no_real_source_flag is not True:
            return ResearchReportDecision.DENY_Z2_REAL_SOURCE_FORBIDDEN
    elif isinstance(evidence, dict):
        if evidence.get("no_real_source_flag") is not True:
            return ResearchReportDecision.DENY_Z2_REAL_SOURCE_FORBIDDEN

    # Check forbidden_outputs_removed
    if not b1_response.forbidden_outputs_removed:
        return ResearchReportDecision.DENY_Z2_OUTPUTS_UNSAFE

    # Check if decision is DENY
    if b1_response.decision.value.startswith("DENY_"):
        return ResearchReportDecision.ALLOW_Z2_DEGRADED_REPORT

    # Check payload for forbidden outputs
    if payload_contains_forbidden_outputs(b1_response):
        return ResearchReportDecision.DENY_Z2_OUTPUTS_UNSAFE

    return ResearchReportDecision.ALLOW_Z2_READONLY_REPORT


def validate_report_section(section: ResearchReportSection) -> ResearchReportDecision:
    """Validate a report section. Never raises."""
    if not isinstance(section, ResearchReportSection):
        return ResearchReportDecision.DENY_Z2_SOURCE_FORBIDDEN
    if section.section_type not in ALLOWED_REPORT_SECTIONS:
        return ResearchReportDecision.DENY_Z2_SOURCE_FORBIDDEN
    if section.confidence_level not in ALLOWED_CONFIDENCE_LEVELS:
        return ResearchReportDecision.DENY_Z2_EVIDENCE_INCOMPLETE
    if not section.readonly_only:
        return ResearchReportDecision.DENY_Z2_EXECUTION_FORBIDDEN
    return ResearchReportDecision.ALLOW_Z2_READONLY_REPORT


def validate_report_response(response: ResearchReportNodeResponse) -> ResearchReportDecision:
    """Validate a full report response. Never raises."""
    if not isinstance(response, ResearchReportNodeResponse):
        return ResearchReportDecision.DENY_Z2_SOURCE_FORBIDDEN
    if not response.readonly_only:
        return ResearchReportDecision.DENY_Z2_EXECUTION_FORBIDDEN
    if not response.no_alpha_claim:
        return ResearchReportDecision.DENY_Z2_OUTPUTS_UNSAFE
    if not response.no_trade_signal:
        return ResearchReportDecision.DENY_Z2_OUTPUTS_UNSAFE
    if not response.no_position_weight:
        return ResearchReportDecision.DENY_Z2_OUTPUTS_UNSAFE
    if not response.forbidden_outputs_removed:
        return ResearchReportDecision.DENY_Z2_OUTPUTS_UNSAFE
    return ResearchReportDecision.ALLOW_Z2_READONLY_REPORT


def validate_z9_snapshot_candidate(
    candidate: Z9ReviewSnapshotCandidate,
) -> ResearchReportDecision:
    """Validate Z9 review snapshot candidate. Never raises."""
    if not isinstance(candidate, Z9ReviewSnapshotCandidate):
        return ResearchReportDecision.DENY_Z2_SOURCE_FORBIDDEN
    if not candidate.readonly_only:
        return ResearchReportDecision.DENY_Z2_EXECUTION_FORBIDDEN
    if not candidate.no_trade_result:
        return ResearchReportDecision.DENY_Z2_OUTPUTS_UNSAFE
    if not candidate.no_paper_trading:
        return ResearchReportDecision.DENY_Z2_OUTPUTS_UNSAFE
    if not candidate.no_broker_action:
        return ResearchReportDecision.DENY_Z2_OUTPUTS_UNSAFE
    if not candidate.no_position_change:
        return ResearchReportDecision.DENY_Z2_OUTPUTS_UNSAFE
    return ResearchReportDecision.ALLOW_Z2_READONLY_REPORT


def validate_no_forbidden_report_outputs(payload) -> ResearchReportDecision:
    """Check payload for forbidden outputs. Never raises."""
    if payload_contains_forbidden_outputs(payload):
        return ResearchReportDecision.DENY_Z2_OUTPUTS_UNSAFE
    return ResearchReportDecision.ALLOW_Z2_READONLY_REPORT
