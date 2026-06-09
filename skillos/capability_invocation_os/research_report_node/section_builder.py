"""Research Report Node section builders — 11 section types."""

import uuid

from skillos.capability_invocation_os.research_report_node.constants import (
    FORBIDDEN_REPORT_OUTPUTS,
)
from skillos.capability_invocation_os.research_report_node.models import (
    ResearchReportSection,
)


def build_report_header_section(source_refs: list = None) -> ResearchReportSection:
    """Build report_header section."""
    return ResearchReportSection(
        section_id=str(uuid.uuid4()),
        section_type="report_header",
        source_refs=source_refs or [],
        evidence_refs=[],
        confidence_level="LOW",
        degradation_status="",
        blocked_outputs_removed=sorted(FORBIDDEN_REPORT_OUTPUTS),
        readonly_only=True,
        no_alpha_claim=True,
        no_trade_signal=True,
    )


def build_source_graph_summary_section(source_refs: list = None, evidence_refs: list = None) -> ResearchReportSection:
    """Build source_graph_summary section."""
    return ResearchReportSection(
        section_id=str(uuid.uuid4()),
        section_type="source_graph_summary",
        source_refs=source_refs or [],
        evidence_refs=evidence_refs or [],
        confidence_level="LOW",
        degradation_status="",
        blocked_outputs_removed=sorted(FORBIDDEN_REPORT_OUTPUTS),
        readonly_only=True,
        no_alpha_claim=True,
        no_trade_signal=True,
    )


def build_factor_context_summary_section(source_refs: list = None, evidence_refs: list = None) -> ResearchReportSection:
    """Build factor_context_summary section."""
    return ResearchReportSection(
        section_id=str(uuid.uuid4()),
        section_type="factor_context_summary",
        source_refs=source_refs or [],
        evidence_refs=evidence_refs or [],
        confidence_level="MEDIUM",
        degradation_status="",
        blocked_outputs_removed=sorted(FORBIDDEN_REPORT_OUTPUTS),
        readonly_only=True,
        no_alpha_claim=True,
        no_trade_signal=True,
    )


def build_evidence_chain_summary_section(source_refs: list = None, evidence_refs: list = None) -> ResearchReportSection:
    """Build evidence_chain_summary section."""
    return ResearchReportSection(
        section_id=str(uuid.uuid4()),
        section_type="evidence_chain_summary",
        source_refs=source_refs or [],
        evidence_refs=evidence_refs or [],
        confidence_level="MEDIUM",
        degradation_status="",
        blocked_outputs_removed=sorted(FORBIDDEN_REPORT_OUTPUTS),
        readonly_only=True,
        no_alpha_claim=True,
        no_trade_signal=True,
    )


def build_structural_readiness_summary_section(source_refs: list = None) -> ResearchReportSection:
    """Build structural_readiness_summary section."""
    return ResearchReportSection(
        section_id=str(uuid.uuid4()),
        section_type="structural_readiness_summary",
        source_refs=source_refs or [],
        evidence_refs=[],
        confidence_level="HIGH_WITH_STRUCTURE_ONLY",
        degradation_status="",
        blocked_outputs_removed=sorted(FORBIDDEN_REPORT_OUTPUTS),
        readonly_only=True,
        no_alpha_claim=True,
        no_trade_signal=True,
    )


def build_research_interpretation_section(source_refs: list = None, evidence_refs: list = None) -> ResearchReportSection:
    """Build research_interpretation section."""
    return ResearchReportSection(
        section_id=str(uuid.uuid4()),
        section_type="research_interpretation",
        source_refs=source_refs or [],
        evidence_refs=evidence_refs or [],
        confidence_level="MEDIUM",
        degradation_status="",
        blocked_outputs_removed=sorted(FORBIDDEN_REPORT_OUTPUTS),
        readonly_only=True,
        no_alpha_claim=True,
        no_trade_signal=True,
    )


def build_risk_warning_section(source_refs: list = None) -> ResearchReportSection:
    """Build risk_warning section."""
    return ResearchReportSection(
        section_id=str(uuid.uuid4()),
        section_type="risk_warning",
        source_refs=source_refs or [],
        evidence_refs=[],
        confidence_level="LOW",
        degradation_status="",
        blocked_outputs_removed=sorted(FORBIDDEN_REPORT_OUTPUTS),
        readonly_only=True,
        no_alpha_claim=True,
        no_trade_signal=True,
    )


def build_missing_evidence_section(missing: list = None) -> ResearchReportSection:
    """Build missing_evidence section."""
    return ResearchReportSection(
        section_id=str(uuid.uuid4()),
        section_type="missing_evidence",
        source_refs=[],
        evidence_refs=missing or [],
        confidence_level="LOW",
        degradation_status="missing",
        blocked_outputs_removed=sorted(FORBIDDEN_REPORT_OUTPUTS),
        readonly_only=True,
        no_alpha_claim=True,
        no_trade_signal=True,
    )


def build_blocked_outputs_removed_section() -> ResearchReportSection:
    """Build blocked_outputs_removed section."""
    return ResearchReportSection(
        section_id=str(uuid.uuid4()),
        section_type="blocked_outputs_removed",
        source_refs=[],
        evidence_refs=[],
        confidence_level="HIGH_WITH_STRUCTURE_ONLY",
        degradation_status="",
        blocked_outputs_removed=sorted(FORBIDDEN_REPORT_OUTPUTS),
        readonly_only=True,
        no_alpha_claim=True,
        no_trade_signal=True,
    )


def build_confidence_section(confidence_level: str = "LOW") -> ResearchReportSection:
    """Build confidence_section."""
    return ResearchReportSection(
        section_id=str(uuid.uuid4()),
        section_type="confidence_section",
        source_refs=[],
        evidence_refs=[],
        confidence_level=confidence_level if confidence_level in ("LOW", "MEDIUM", "HIGH_WITH_STRUCTURE_ONLY") else "LOW",
        degradation_status="",
        blocked_outputs_removed=sorted(FORBIDDEN_REPORT_OUTPUTS),
        readonly_only=True,
        no_alpha_claim=True,
        no_trade_signal=True,
    )


def build_next_validation_requirement_section() -> ResearchReportSection:
    """Build next_validation_requirement section."""
    return ResearchReportSection(
        section_id=str(uuid.uuid4()),
        section_type="next_validation_requirement",
        source_refs=[],
        evidence_refs=[],
        confidence_level="LOW",
        degradation_status="",
        blocked_outputs_removed=sorted(FORBIDDEN_REPORT_OUTPUTS),
        readonly_only=True,
        no_alpha_claim=True,
        no_trade_signal=True,
    )
