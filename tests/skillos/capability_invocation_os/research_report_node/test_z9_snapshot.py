"""Tests for Z9 review snapshot candidate."""

from skillos.capability_invocation_os.research_report_node.constants import (
    FORBIDDEN_REPORT_OUTPUTS,
)
from skillos.capability_invocation_os.research_report_node.models import (
    ResearchReportDecision,
    Z9ReviewSnapshotCandidate,
)
from skillos.capability_invocation_os.research_report_node.z9_snapshot import (
    build_z9_review_snapshot_candidate,
    validate_z9_review_snapshot_candidate,
)


def test_build_z9_candidate_defaults():
    """build_z9_review_snapshot_candidate returns valid candidate."""
    c = build_z9_review_snapshot_candidate()
    assert isinstance(c, Z9ReviewSnapshotCandidate)
    assert c.readonly_only is True
    assert c.no_trade_result is True
    assert c.no_paper_trading is True
    assert c.no_broker_action is True
    assert c.no_position_change is True


def test_build_z9_candidate_with_params():
    """build_z9_review_snapshot_candidate passes custom params."""
    c = build_z9_review_snapshot_candidate(
        report_node_id="rn-1",
        confidence_level="MEDIUM",
        review_required=True,
        review_reason="test review",
    )
    assert c.report_node_id == "rn-1"
    assert c.confidence_level == "MEDIUM"
    assert c.review_required is True
    assert c.review_reason == "test review"


def test_build_z9_candidate_invalid_confidence_defaults_low():
    """Invalid confidence_level defaults to LOW."""
    c = build_z9_review_snapshot_candidate(confidence_level="EXTREME")
    assert c.confidence_level == "LOW"


def test_build_z9_candidate_has_forbidden_outputs():
    """Candidate blocked_outputs_removed contains all forbidden outputs."""
    c = build_z9_review_snapshot_candidate()
    assert set(c.blocked_outputs_removed) == FORBIDDEN_REPORT_OUTPUTS


def test_build_z9_candidate_missing_evidence():
    """Missing evidence list is stored."""
    c = build_z9_review_snapshot_candidate(missing_evidence=["a", "b"])
    assert c.missing_evidence == ["a", "b"]


def test_validate_z9_candidate_allows_valid():
    """Valid candidate → ALLOW_Z2_READONLY_REPORT."""
    c = build_z9_review_snapshot_candidate()
    assert validate_z9_review_snapshot_candidate(c) == ResearchReportDecision.ALLOW_Z2_READONLY_REPORT


def test_validate_z9_candidate_denies_non_candidate():
    """Non-candidate object → DENY_Z2_SOURCE_FORBIDDEN."""
    assert validate_z9_review_snapshot_candidate("not a candidate") == ResearchReportDecision.DENY_Z2_SOURCE_FORBIDDEN


def test_validate_z9_candidate_denies_non_readonly():
    """readonly_only=False → DENY_Z2_EXECUTION_FORBIDDEN."""
    c = Z9ReviewSnapshotCandidate(readonly_only=False)
    assert validate_z9_review_snapshot_candidate(c) == ResearchReportDecision.DENY_Z2_EXECUTION_FORBIDDEN


def test_validate_z9_candidate_denies_trade_result():
    """no_trade_result=False → DENY_Z2_OUTPUTS_UNSAFE."""
    c = Z9ReviewSnapshotCandidate(no_trade_result=False)
    assert validate_z9_review_snapshot_candidate(c) == ResearchReportDecision.DENY_Z2_OUTPUTS_UNSAFE


def test_validate_z9_candidate_denies_paper_trading():
    """no_paper_trading=False → DENY_Z2_OUTPUTS_UNSAFE."""
    c = Z9ReviewSnapshotCandidate(no_paper_trading=False)
    assert validate_z9_review_snapshot_candidate(c) == ResearchReportDecision.DENY_Z2_OUTPUTS_UNSAFE


def test_validate_z9_candidate_denies_broker_action():
    """no_broker_action=False → DENY_Z2_OUTPUTS_UNSAFE."""
    c = Z9ReviewSnapshotCandidate(no_broker_action=False)
    assert validate_z9_review_snapshot_candidate(c) == ResearchReportDecision.DENY_Z2_OUTPUTS_UNSAFE
