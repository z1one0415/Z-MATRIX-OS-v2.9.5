"""Tests for ResearchReportNode builder class."""

from unittest.mock import patch

from skillos.capability_invocation_os.composition_graph.models import (
    CompositionGraphResponse,
    CompositionGraphDecision,
    CompositionGraphEvidence,
)
from skillos.capability_invocation_os.research_report_node.constants import (
    FORBIDDEN_REPORT_OUTPUTS,
)
from skillos.capability_invocation_os.research_report_node.models import (
    ResearchReportDecision,
    ResearchReportNodeRequest,
    ResearchReportNodeResponse,
)
from skillos.capability_invocation_os.research_report_node.report_builder import (
    ResearchReportNode,
)


def _make_valid_b1_evidence():
    return CompositionGraphEvidence(
        source_class="factor_library_fixture",
        no_real_source_flag=True,
        fixture_source_commit="P1_FIXTURE_ONLY",
        graph_node_hash="n",
        graph_edge_hash="e",
        permission_tier="T0",
        forbidden_outputs_removed_hash="h",
        rollback_marker=False,
        privacy_marker=True,
        c1_handoff_marker=True,
    )


def _make_valid_b1_response():
    return CompositionGraphResponse(
        response_id="b1-builder-test",
        decision=CompositionGraphDecision.ALLOW_GRAPH_READONLY_SUMMARY,
        evidence=_make_valid_b1_evidence(),
        forbidden_outputs_removed=sorted(FORBIDDEN_REPORT_OUTPUTS),
        degraded=False,
        mode="DISABLED_DEFAULT_P0",
        graph_enabled=False,
        execution_enabled=False,
    )


def test_default_node_returns_noop():
    """Default node without mocking returns NOOP."""
    node = ResearchReportNode()
    resp = node.build_report_from_b1_graph(_make_valid_b1_response())
    assert resp.decision == ResearchReportDecision.DISABLED_DEFAULT_NOOP


def test_disabled_default_response():
    """build_disabled_default_response returns correct shape."""
    node = ResearchReportNode()
    resp = node.build_disabled_default_response()
    assert resp.decision == ResearchReportDecision.DISABLED_DEFAULT_NOOP
    assert resp.readonly_only is True
    assert resp.mode == "DISABLED_DEFAULT_P0"
    assert set(resp.forbidden_outputs_removed) == FORBIDDEN_REPORT_OUTPUTS


def test_degraded_report():
    """build_degraded_report returns degraded=True with given decision."""
    node = ResearchReportNode()
    resp = node.build_degraded_report(ResearchReportDecision.DENY_Z2_SOURCE_FORBIDDEN)
    assert resp.decision == ResearchReportDecision.DENY_Z2_SOURCE_FORBIDDEN
    assert resp.degraded is True
    assert resp.readonly_only is True


@patch("skillos.capability_invocation_os.research_report_node.report_builder.should_force_disabled", return_value=False)
@patch("skillos.capability_invocation_os.research_report_node.report_builder.is_research_report_node_enabled", return_value=True)
def test_build_report_full_with_valid_b1(mock_enabled, mock_killed):
    """Full build with valid B1 → ALLOW_Z2_READONLY_REPORT."""
    node = ResearchReportNode(fixture_mode=True)
    resp = node.build_report_from_b1_graph(_make_valid_b1_response())
    assert resp.decision == ResearchReportDecision.ALLOW_Z2_READONLY_REPORT
    assert resp.readonly_only is True
    assert resp.report_enabled is True
    assert len(resp.sections) == 11


@patch("skillos.capability_invocation_os.research_report_node.report_builder.should_force_disabled", return_value=False)
@patch("skillos.capability_invocation_os.research_report_node.report_builder.is_research_report_node_enabled", return_value=True)
def test_build_report_denies_execution_request(mock_enabled, mock_killed):
    """Execution requested → DENY_Z2_EXECUTION_FORBIDDEN."""
    node = ResearchReportNode(fixture_mode=True)
    req = ResearchReportNodeRequest(execution_requested=True)
    resp = node.build_report_from_b1_graph(_make_valid_b1_response(), request=req)
    assert resp.decision == ResearchReportDecision.DENY_Z2_EXECUTION_FORBIDDEN
    assert resp.degraded is True


@patch("skillos.capability_invocation_os.research_report_node.report_builder.should_force_disabled", return_value=False)
@patch("skillos.capability_invocation_os.research_report_node.report_builder.is_research_report_node_enabled", return_value=True)
def test_build_report_denies_non_b1_source(mock_enabled, mock_killed):
    """Non-CompositionGraphResponse → DENY_Z2_SOURCE_FORBIDDEN."""
    node = ResearchReportNode(fixture_mode=True)
    resp = node.build_report_from_b1_graph({"fake": True})
    assert resp.decision == ResearchReportDecision.DENY_Z2_SOURCE_FORBIDDEN


@patch("skillos.capability_invocation_os.research_report_node.report_builder.should_force_disabled", return_value=False)
@patch("skillos.capability_invocation_os.research_report_node.report_builder.is_research_report_node_enabled", return_value=True)
def test_build_report_degraded_on_deny_b1_decision(mock_enabled, mock_killed):
    """B1 DENY decision → ALLOW_Z2_DEGRADED_REPORT."""
    resp_b1 = CompositionGraphResponse(
        response_id="deny-b1",
        decision=CompositionGraphDecision.DENY_GRAPH_SOURCE_FORBIDDEN,
        evidence=_make_valid_b1_evidence(),
        forbidden_outputs_removed=sorted(FORBIDDEN_REPORT_OUTPUTS),
    )
    node = ResearchReportNode(fixture_mode=True)
    resp = node.build_report_from_b1_graph(resp_b1)
    assert resp.decision == ResearchReportDecision.ALLOW_Z2_DEGRADED_REPORT
    assert resp.degraded is True


@patch("skillos.capability_invocation_os.research_report_node.report_builder.should_force_disabled", return_value=False)
@patch("skillos.capability_invocation_os.research_report_node.report_builder.is_research_report_node_enabled", return_value=True)
def test_build_report_all_sections_readonly(mock_enabled, mock_killed):
    """All sections in full report have readonly_only=True."""
    node = ResearchReportNode(fixture_mode=True)
    resp = node.build_report_from_b1_graph(_make_valid_b1_response())
    for section in resp.sections:
        assert section.readonly_only is True
        assert section.no_alpha_claim is True
        assert section.no_trade_signal is True


def test_no_forbidden_method_names():
    """ResearchReportNode has no forbidden method names."""
    from skillos.capability_invocation_os.research_report_node.constants import FORBIDDEN_METHOD_NAMES
    node = ResearchReportNode()
    methods = [m for m in dir(node) if not m.startswith("_")]
    for method in methods:
        assert method not in FORBIDDEN_METHOD_NAMES, f"Forbidden method: {method}"
