"""Research Report Node Z9 review snapshot candidate builder."""

from skillos.capability_invocation_os.research_report_node.constants import (
    FORBIDDEN_REPORT_OUTPUTS,
)
from skillos.capability_invocation_os.research_report_node.models import (
    ResearchReportDecision,
    Z9ReviewSnapshotCandidate,
)


def build_z9_review_snapshot_candidate(
    report_node_id: str = "",
    source_graph_hash: str = "",
    factor_context_summary_hash: str = "",
    evidence_chain_hash: str = "",
    research_summary_hash: str = "",
    risk_warning_hash: str = "",
    confidence_level: str = "LOW",
    confidence_reason: str = "",
    missing_evidence: list = None,
    degradation_status: str = "",
    review_required: bool = False,
    review_reason: str = "",
) -> Z9ReviewSnapshotCandidate:
    """Build a Z9ReviewSnapshotCandidate. Never raises."""
    return Z9ReviewSnapshotCandidate(
        report_node_id=report_node_id,
        source_graph_hash=source_graph_hash,
        factor_context_summary_hash=factor_context_summary_hash,
        evidence_chain_hash=evidence_chain_hash,
        research_summary_hash=research_summary_hash,
        risk_warning_hash=risk_warning_hash,
        confidence_level=confidence_level if confidence_level in ("LOW", "MEDIUM", "HIGH_WITH_STRUCTURE_ONLY") else "LOW",
        confidence_reason=confidence_reason,
        missing_evidence=missing_evidence or [],
        degradation_status=degradation_status,
        blocked_outputs_removed=sorted(FORBIDDEN_REPORT_OUTPUTS),
        review_required=review_required,
        review_reason=review_reason,
        readonly_only=True,
        no_trade_result=True,
        no_paper_trading=True,
        no_broker_action=True,
        no_position_change=True,
    )


def validate_z9_review_snapshot_candidate(
    candidate: Z9ReviewSnapshotCandidate,
) -> ResearchReportDecision:
    """Validate a Z9ReviewSnapshotCandidate. Never raises."""
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
