"""Tests for Research Report Node degradation builders."""

from skillos.capability_invocation_os.research_report_node.models import (
    ResearchReportDecision,
)
from skillos.capability_invocation_os.research_report_node.degradation import (
    build_allow_readonly_report_decision,
    build_allow_degraded_report_decision,
    build_deny_source_forbidden_decision,
    build_deny_real_source_forbidden_decision,
    build_deny_outputs_unsafe_decision,
    build_deny_graph_denied_decision,
    build_deny_evidence_incomplete_decision,
    build_deny_execution_forbidden_decision,
    build_disabled_default_noop_decision,
)


def test_allow_readonly():
    """build_allow_readonly_report_decision returns correct enum."""
    assert build_allow_readonly_report_decision() == ResearchReportDecision.ALLOW_Z2_READONLY_REPORT


def test_allow_degraded():
    """build_allow_degraded_report_decision returns correct enum."""
    assert build_allow_degraded_report_decision() == ResearchReportDecision.ALLOW_Z2_DEGRADED_REPORT


def test_deny_source_forbidden():
    """build_deny_source_forbidden_decision returns correct enum."""
    assert build_deny_source_forbidden_decision() == ResearchReportDecision.DENY_Z2_SOURCE_FORBIDDEN


def test_deny_real_source_forbidden():
    """build_deny_real_source_forbidden_decision returns correct enum."""
    assert build_deny_real_source_forbidden_decision() == ResearchReportDecision.DENY_Z2_REAL_SOURCE_FORBIDDEN


def test_deny_outputs_unsafe():
    """build_deny_outputs_unsafe_decision returns correct enum."""
    assert build_deny_outputs_unsafe_decision() == ResearchReportDecision.DENY_Z2_OUTPUTS_UNSAFE


def test_disabled_default_noop():
    """build_disabled_default_noop_decision returns DISABLED_DEFAULT_NOOP."""
    assert build_disabled_default_noop_decision() == ResearchReportDecision.DISABLED_DEFAULT_NOOP
