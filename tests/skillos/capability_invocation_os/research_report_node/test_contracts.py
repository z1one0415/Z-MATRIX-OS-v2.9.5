"""Tests for Research Report Node contracts."""

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
    ResearchReportSection,
    Z9ReviewSnapshotCandidate,
)
from skillos.capability_invocation_os.research_report_node.contracts import (
    validate_report_request,
    validate_b1_graph_response_for_report,
    validate_report_section,
    validate_report_response,
    validate_z9_snapshot_candidate,
    validate_no_forbidden_report_outputs,
    payload_contains_forbidden_outputs,
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
        response_id="b1-test-123",
        decision=CompositionGraphDecision.ALLOW_GRAPH_READONLY_SUMMARY,
        evidence=_make_valid_b1_evidence(),
        forbidden_outputs_removed=sorted(FORBIDDEN_REPORT_OUTPUTS),
        degraded=False,
        mode="DISABLED_DEFAULT_P0",
        graph_enabled=False,
        execution_enabled=False,
    )


def test_validate_request_allows_readonly():
    """Valid readonly request → ALLOW_Z2_READONLY_REPORT."""
    req = ResearchReportNodeRequest(request_id="r1", intent="Z2_READONLY_REPORT")
    assert validate_report_request(req) == ResearchReportDecision.ALLOW_Z2_READONLY_REPORT


def test_validate_request_denies_execution():
    """execution_requested=True → DENY_Z2_EXECUTION_FORBIDDEN."""
    req = ResearchReportNodeRequest(request_id="r2", execution_requested=True)
    assert validate_report_request(req) == ResearchReportDecision.DENY_Z2_EXECUTION_FORBIDDEN


def test_validate_request_denies_non_request():
    """Non-request object → DENY_Z2_SOURCE_FORBIDDEN."""
    assert validate_report_request("not a request") == ResearchReportDecision.DENY_Z2_SOURCE_FORBIDDEN


def test_validate_b1_allows_valid():
    """Valid B1 response → ALLOW_Z2_READONLY_REPORT."""
    result = validate_b1_graph_response_for_report(_make_valid_b1_response())
    assert result == ResearchReportDecision.ALLOW_Z2_READONLY_REPORT


def test_validate_b1_denies_non_response():
    """Non-CompositionGraphResponse → DENY_Z2_SOURCE_FORBIDDEN."""
    result = validate_b1_graph_response_for_report({"fake": True})
    assert result == ResearchReportDecision.DENY_Z2_SOURCE_FORBIDDEN


def test_validate_b1_denies_real_source():
    """no_real_source_flag=False → DENY_Z2_REAL_SOURCE_FORBIDDEN."""
    bad_evidence = CompositionGraphEvidence(no_real_source_flag=False)
    resp = CompositionGraphResponse(
        response_id="bad",
        decision=CompositionGraphDecision.ALLOW_GRAPH_READONLY_SUMMARY,
        evidence=bad_evidence,
        forbidden_outputs_removed=sorted(FORBIDDEN_REPORT_OUTPUTS),
    )
    result = validate_b1_graph_response_for_report(resp)
    assert result == ResearchReportDecision.DENY_Z2_REAL_SOURCE_FORBIDDEN


def test_validate_b1_denies_missing_forbidden_outputs():
    """Empty forbidden_outputs_removed → DENY_Z2_OUTPUTS_UNSAFE."""
    resp = CompositionGraphResponse(
        response_id="bad2",
        decision=CompositionGraphDecision.ALLOW_GRAPH_READONLY_SUMMARY,
        evidence=_make_valid_b1_evidence(),
        forbidden_outputs_removed=[],
    )
    result = validate_b1_graph_response_for_report(resp)
    assert result == ResearchReportDecision.DENY_Z2_OUTPUTS_UNSAFE


def test_validate_b1_allows_degraded_on_deny_decision():
    """B1 DENY decision → ALLOW_Z2_DEGRADED_REPORT."""
    resp = CompositionGraphResponse(
        response_id="deny1",
        decision=CompositionGraphDecision.DENY_GRAPH_SOURCE_FORBIDDEN,
        evidence=_make_valid_b1_evidence(),
        forbidden_outputs_removed=sorted(FORBIDDEN_REPORT_OUTPUTS),
    )
    result = validate_b1_graph_response_for_report(resp)
    assert result == ResearchReportDecision.ALLOW_Z2_DEGRADED_REPORT


def test_validate_section_allows_valid():
    """Valid section → ALLOW_Z2_READONLY_REPORT."""
    s = ResearchReportSection(section_type="report_header", confidence_level="LOW")
    assert validate_report_section(s) == ResearchReportDecision.ALLOW_Z2_READONLY_REPORT


def test_validate_section_denies_invalid_type():
    """Invalid section_type → DENY_Z2_SOURCE_FORBIDDEN."""
    s = ResearchReportSection(section_type="alpha_generator", confidence_level="LOW")
    assert validate_report_section(s) == ResearchReportDecision.DENY_Z2_SOURCE_FORBIDDEN


def test_validate_response_allows_valid():
    """Valid response → ALLOW_Z2_READONLY_REPORT."""
    resp = ResearchReportNodeResponse()
    assert validate_report_response(resp) == ResearchReportDecision.ALLOW_Z2_READONLY_REPORT


def test_payload_contains_forbidden_detects_nested():
    """payload_contains_forbidden_outputs detects nested forbidden keys."""
    payload = {"data": {"nested": {"alpha_claim": "bad"}}}
    assert payload_contains_forbidden_outputs(payload) is True
    clean = {"data": {"nested": {"clean_key": "ok"}}}
    assert payload_contains_forbidden_outputs(clean) is False
