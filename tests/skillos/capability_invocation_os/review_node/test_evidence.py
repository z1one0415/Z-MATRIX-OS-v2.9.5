"""Tests for Z9 evidence."""
import uuid
from skillos.capability_invocation_os.research_report_node.models import Z9ReviewSnapshotCandidate
from skillos.capability_invocation_os.review_node.evidence import (
    build_z9_review_evidence_from_z2_snapshot,
    build_z9_review_node_hash, build_z9_review_section_hash, build_z9_feedback_candidate_hash,
)
from skillos.capability_invocation_os.review_node.models import Z9ReviewDecision

def _make_snapshot(**kwargs):
    defaults = dict(
        report_node_id="r1", source_graph_hash="gh1", evidence_chain_hash="ech1",
        research_summary_hash="rsh1", risk_warning_hash="rwh1",
        confidence_level="LOW", degradation_status="", readonly_only=True,
        blocked_outputs_removed=["alpha_claim", "trade_result"],
        review_required=False,
    )
    defaults.update(kwargs)
    return Z9ReviewSnapshotCandidate(**defaults)

def test_evidence_inherits_source_graph_hash():
    snapshot = _make_snapshot(source_graph_hash="graph_abc")
    evidence = build_z9_review_evidence_from_z2_snapshot(snapshot)
    assert evidence.source_graph_hash == "graph_abc"

def test_evidence_inherits_evidence_chain_hash():
    snapshot = _make_snapshot(evidence_chain_hash="chain_abc")
    evidence = build_z9_review_evidence_from_z2_snapshot(snapshot)
    assert evidence.evidence_chain_hash == "chain_abc"

def test_evidence_inherits_research_summary_hash():
    snapshot = _make_snapshot(research_summary_hash="res_abc")
    evidence = build_z9_review_evidence_from_z2_snapshot(snapshot)
    assert evidence.research_summary_hash == "res_abc"

def test_evidence_inherits_risk_warning_hash():
    snapshot = _make_snapshot(risk_warning_hash="risk_abc")
    evidence = build_z9_review_evidence_from_z2_snapshot(snapshot)
    assert evidence.risk_warning_hash == "risk_abc"

def test_evidence_inherits_confidence():
    snapshot = _make_snapshot(confidence_level="MEDIUM")
    evidence = build_z9_review_evidence_from_z2_snapshot(snapshot)
    assert evidence.confidence_level == "MEDIUM"

def test_evidence_generates_review_node_hash():
    snapshot = _make_snapshot()
    evidence = build_z9_review_evidence_from_z2_snapshot(snapshot)
    assert evidence.z9_review_node_hash != ""

def test_evidence_generates_section_hash():
    snapshot = _make_snapshot()
    h = build_z9_review_section_hash("s1", "test")
    assert isinstance(h, str) and len(h) == 64

def test_evidence_generates_feedback_hash():
    h = build_z9_feedback_candidate_hash("f1", "REVIEW")
    assert isinstance(h, str) and len(h) == 64

def test_evidence_missing_not_valid():
    snapshot = _make_snapshot()
    evidence = build_z9_review_evidence_from_z2_snapshot(snapshot)
    assert evidence.privacy_marker is True
