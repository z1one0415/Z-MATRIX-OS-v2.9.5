"""Research Report Node degradation builders — one per decision type."""

import uuid

from skillos.capability_invocation_os.research_report_node.models import (
    ResearchReportDecision,
)


def build_allow_readonly_report_decision() -> ResearchReportDecision:
    """Build ALLOW_Z2_READONLY_REPORT decision."""
    return ResearchReportDecision.ALLOW_Z2_READONLY_REPORT


def build_allow_degraded_report_decision() -> ResearchReportDecision:
    """Build ALLOW_Z2_DEGRADED_REPORT decision."""
    return ResearchReportDecision.ALLOW_Z2_DEGRADED_REPORT


def build_deny_source_forbidden_decision() -> ResearchReportDecision:
    """Build DENY_Z2_SOURCE_FORBIDDEN decision."""
    return ResearchReportDecision.DENY_Z2_SOURCE_FORBIDDEN


def build_deny_real_source_forbidden_decision() -> ResearchReportDecision:
    """Build DENY_Z2_REAL_SOURCE_FORBIDDEN decision."""
    return ResearchReportDecision.DENY_Z2_REAL_SOURCE_FORBIDDEN


def build_deny_outputs_unsafe_decision() -> ResearchReportDecision:
    """Build DENY_Z2_OUTPUTS_UNSAFE decision."""
    return ResearchReportDecision.DENY_Z2_OUTPUTS_UNSAFE


def build_deny_graph_denied_decision() -> ResearchReportDecision:
    """Build DENY_Z2_GRAPH_DENIED decision."""
    return ResearchReportDecision.DENY_Z2_GRAPH_DENIED


def build_deny_evidence_incomplete_decision() -> ResearchReportDecision:
    """Build DENY_Z2_EVIDENCE_INCOMPLETE decision."""
    return ResearchReportDecision.DENY_Z2_EVIDENCE_INCOMPLETE


def build_deny_execution_forbidden_decision() -> ResearchReportDecision:
    """Build DENY_Z2_EXECUTION_FORBIDDEN decision."""
    return ResearchReportDecision.DENY_Z2_EXECUTION_FORBIDDEN


def build_disabled_default_noop_decision() -> ResearchReportDecision:
    """Build DISABLED_DEFAULT_NOOP decision."""
    return ResearchReportDecision.DISABLED_DEFAULT_NOOP
