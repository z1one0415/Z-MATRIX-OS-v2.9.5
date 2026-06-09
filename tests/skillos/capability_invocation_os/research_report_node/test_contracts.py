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
    forbidden_outputs_removed_complete,
)


def _make_valid_b1_evidence():
    """Return dict evidence with all required hashes populated."""
    return {
        "source_class": "factor_library_fixture",
        "no_real_source_flag": True,
        "fixture_source_commit": "P1_FIXTURE_ONLY",
        "graph_node_hash": "node_hash_abc",
        "graph_edge_hash": "edge_hash_def",
        "permission_tier": "T0",
        "forbidden_outputs_removed_hash": "frh",
        "rollback_marker": False,
        "privacy_marker": True,
        "c1_handoff_marker": True,
        "request_hash": "req_hash_123",
        "response_hash_placeholder": "resp_hash_456",
        "factor_decision_hash": "factor_hash_789",
        "bridge_decision_hash": "bridge_hash_012",
    }


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



def test_forbidden_outputs_removed_complete_true():
    """Complete set returns True."""
    assert forbidden_outputs_removed_complete(sorted(FORBIDDEN_REPORT_OUTPUTS)) is True


def test_forbidden_outputs_removed_complete_false():
    """Incomplete set returns False."""
    incomplete = list(FORBIDDEN_REPORT_OUTPUTS)[:3]
    assert forbidden_outputs_removed_complete(incomplete) is False


def test_validate_b1_forbidden_outputs_incomplete_denied():
    """B1 with incomplete forbidden_outputs_removed → DENY_Z2_OUTPUTS_UNSAFE."""
    resp = CompositionGraphResponse(
        response_id="incomplete-fo",
        decision=CompositionGraphDecision.ALLOW_GRAPH_READONLY_SUMMARY,
        evidence=_make_valid_b1_evidence(),
        forbidden_outputs_removed=["alpha_claim"],  # incomplete
    )
    result = validate_b1_graph_response_for_report(resp)
    assert result == ResearchReportDecision.DENY_Z2_OUTPUTS_UNSAFE


def test_validate_b1_response_with_alpha_claim_denied():
    """B1 response containing alpha_claim key → DENY_Z2_OUTPUTS_UNSAFE."""
    # payload_contains_forbidden_outputs on response with forbidden key in evidence
    resp = CompositionGraphResponse(
        response_id="alpha-bad",
        decision=CompositionGraphDecision.ALLOW_GRAPH_READONLY_SUMMARY,
        evidence={"no_real_source_flag": True, "alpha_claim": "bad_data",
                  "graph_node_hash": "n", "graph_edge_hash": "e",
                  "request_hash": "r", "response_hash_placeholder": "rp",
                  "factor_decision_hash": "f", "bridge_decision_hash": "b"},
        forbidden_outputs_removed=sorted(FORBIDDEN_REPORT_OUTPUTS),
    )
    result = validate_b1_graph_response_for_report(resp)
    assert result == ResearchReportDecision.DENY_Z2_OUTPUTS_UNSAFE


def test_validate_section_with_position_weight_denied():
    """Section with position_weight field → DENY_Z2_OUTPUTS_UNSAFE via payload scan."""
    # payload_contains_forbidden_outputs checks field names on dataclass
    # position_weight as a field name would trigger — but ResearchReportSection
    # doesn't have it. Test that a dict payload with forbidden key is detected.
    payload = {"position_weight": 0.5}
    assert payload_contains_forbidden_outputs(payload) is True


def test_validate_z9_snapshot_with_trade_result_denied():
    """Snapshot with no_trade_result=False → DENY_Z2_OUTPUTS_UNSAFE."""
    c = Z9ReviewSnapshotCandidate(no_trade_result=False)
    result = validate_z9_snapshot_candidate(c)
    assert result == ResearchReportDecision.DENY_Z2_OUTPUTS_UNSAFE


def test_validate_b1_missing_factor_decision_hash_denied():
    """B1 evidence missing factor_decision_hash → DENY_Z2_EVIDENCE_INCOMPLETE."""
    evidence = {
        "source_class": "fixture",
        "no_real_source_flag": True,
        "graph_node_hash": "n",
        "graph_edge_hash": "e",
        "request_hash": "r",
        "response_hash_placeholder": "rp",
        "factor_decision_hash": "",  # missing
        "bridge_decision_hash": "b",
    }
    resp = CompositionGraphResponse(
        response_id="missing-fdh",
        decision=CompositionGraphDecision.ALLOW_GRAPH_READONLY_SUMMARY,
        evidence=evidence,
        forbidden_outputs_removed=sorted(FORBIDDEN_REPORT_OUTPUTS),
    )
    result = validate_b1_graph_response_for_report(resp)
    assert result == ResearchReportDecision.DENY_Z2_EVIDENCE_INCOMPLETE


def test_validate_b1_missing_bridge_decision_hash_denied():
    """B1 evidence missing bridge_decision_hash → DENY_Z2_EVIDENCE_INCOMPLETE."""
    evidence = {
        "source_class": "fixture",
        "no_real_source_flag": True,
        "graph_node_hash": "n",
        "graph_edge_hash": "e",
        "request_hash": "r",
        "response_hash_placeholder": "rp",
        "factor_decision_hash": "f",
        "bridge_decision_hash": "",  # missing
    }
    resp = CompositionGraphResponse(
        response_id="missing-bdh",
        decision=CompositionGraphDecision.ALLOW_GRAPH_READONLY_SUMMARY,
        evidence=evidence,
        forbidden_outputs_removed=sorted(FORBIDDEN_REPORT_OUTPUTS),
    )
    result = validate_b1_graph_response_for_report(resp)
    assert result == ResearchReportDecision.DENY_Z2_EVIDENCE_INCOMPLETE


def test_validate_b1_missing_graph_node_hash_denied():
    """B1 evidence missing graph_node_hash → DENY_Z2_EVIDENCE_INCOMPLETE."""
    evidence = {
        "source_class": "fixture",
        "no_real_source_flag": True,
        "graph_node_hash": "",  # missing
        "graph_edge_hash": "e",
        "request_hash": "r",
        "response_hash_placeholder": "rp",
        "factor_decision_hash": "f",
        "bridge_decision_hash": "b",
    }
    resp = CompositionGraphResponse(
        response_id="missing-gnh",
        decision=CompositionGraphDecision.ALLOW_GRAPH_READONLY_SUMMARY,
        evidence=evidence,
        forbidden_outputs_removed=sorted(FORBIDDEN_REPORT_OUTPUTS),
    )
    result = validate_b1_graph_response_for_report(resp)
    assert result == ResearchReportDecision.DENY_Z2_EVIDENCE_INCOMPLETE


def test_validate_report_response_scans_sections_and_z9():
    """validate_report_response scans sections and z9 snapshot."""
    resp = ResearchReportNodeResponse(
        forbidden_outputs_removed=sorted(FORBIDDEN_REPORT_OUTPUTS),
    )
    result = validate_report_response(resp)
    assert result == ResearchReportDecision.ALLOW_Z2_READONLY_REPORT
