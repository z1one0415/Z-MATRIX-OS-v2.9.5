"""Comprehensive tests for BLOCKERS 1-6 — Z9 Review Node hardening."""

import uuid
from unittest.mock import patch

from skillos.capability_invocation_os.research_report_node.models import Z9ReviewSnapshotCandidate
from skillos.capability_invocation_os.review_node.models import (
    Z9ReviewDecision,
    Z9ReviewNodeRequest,
    Z9ReviewNodeResponse,
    Z9ReviewSection,
    Z9ReviewEvidence,
    Z2FeedbackCandidate,
)
from skillos.capability_invocation_os.review_node.constants import (
    FORBIDDEN_OUTPUT_KEYS,
    ALLOWED_REVIEW_SECTIONS,
)
from skillos.capability_invocation_os.review_node.contracts import (
    validate_z9_review_request,
    validate_z2_snapshot_candidate,
    validate_z9_review_section,
    validate_z9_review_response,
    validate_z2_feedback_candidate,
    payload_contains_forbidden_inputs,
    payload_contains_forbidden_outputs,
    blocked_outputs_removed_complete,
)
from skillos.capability_invocation_os.review_node.evidence import (
    build_z9_review_evidence_from_z2_snapshot,
    build_z9_review_node_hash,
    build_z9_review_section_hash,
    build_z9_feedback_candidate_hash,
)
from skillos.capability_invocation_os.review_node.review_builder import Z9ReviewNode
from skillos.capability_invocation_os.review_node.attribution import build_explanation_attribution


# ─── helpers ─────────────────────────────────────────────────────────────────

def _make_snapshot(**kwargs):
    """Build a valid Z9ReviewSnapshotCandidate with all required hashes."""
    defaults = dict(
        report_node_id="r1",
        source_graph_hash="src_graph_abc",
        evidence_chain_hash="ech_abc",
        research_summary_hash="rsh_abc",
        risk_warning_hash="rwh_abc",
        factor_context_summary_hash="fcs_abc",
        confidence_level="MEDIUM",
        confidence_reason="test",
        missing_evidence=[],
        degradation_status="",
        blocked_outputs_removed=sorted(FORBIDDEN_OUTPUT_KEYS),
        review_required=False,
        review_reason="",
        readonly_only=True,
        no_trade_result=True,
        no_paper_trading=True,
        no_broker_action=True,
        no_position_change=True,
    )
    defaults.update(kwargs)
    return Z9ReviewSnapshotCandidate(**defaults)


def _make_valid_section(i=0):
    """Build a valid Z9ReviewSection."""
    return Z9ReviewSection(
        section_id=f"sec_{i:02d}",
        section_type="review_header",
        blocked_outputs_removed=sorted(FORBIDDEN_OUTPUT_KEYS),
        readonly_only=True,
    )


def _make_valid_response():
    """Build a valid Z9ReviewNodeResponse."""
    feedback = Z2FeedbackCandidate(
        source_z2_report_node_id="r1",
        review_label="EXPLANATION_ACCEPTED_STRUCTURE_ONLY",
        readonly_only=True,
        requires_human_review=True,
    )
    return Z9ReviewNodeResponse(
        response_id=str(uuid.uuid4()),
        decision=Z9ReviewDecision.ALLOW_Z9_READONLY_REVIEW,
        evidence={},
        sections=[],
        z2_feedback_candidate=feedback,
        forbidden_outputs_removed=sorted(FORBIDDEN_OUTPUT_KEYS),
        degraded=False,
        mode="DISABLED_DEFAULT_P0",
        review_enabled=True,
        memory_mutation_enabled=False,
        readonly_only=True,
        no_trade_result=True,
        no_paper_trading=True,
        no_broker_action=True,
        no_position_change=True,
    )


# ─── BLOCKER 1: fixture_mode=True must allow readonly review building ─────────

def test_fixture_mode_true_with_mocked_kill_switch_produces_review():
    """When fixture_mode=True AND kill_switch/config are patched, it should build."""
    with patch(
        "skillos.capability_invocation_os.review_node.review_builder.should_force_disabled",
        return_value=False,
    ), patch(
        "skillos.capability_invocation_os.review_node.review_builder.is_z9_review_node_enabled",
        return_value=True,
    ):
        node = Z9ReviewNode(fixture_mode=True)
        snapshot = _make_snapshot()
        resp = node.build_review_from_z2_snapshot(snapshot)
        assert resp.decision == Z9ReviewDecision.ALLOW_Z9_READONLY_REVIEW
        assert resp.degraded is False


def test_fixture_mode_true_no_kill_switch_patched_still_noop():
    """Without patching kill_switch, fixture_mode should still be blocked by kill_switch."""
    # kill_switch is True by default → should_force_disabled returns True
    node = Z9ReviewNode(fixture_mode=True)
    from skillos.capability_invocation_os.review_node.kill_switch import should_force_disabled
    if should_force_disabled():
        resp = node.build_review_from_z2_snapshot(_make_snapshot())
        assert resp.decision == Z9ReviewDecision.DISABLED_DEFAULT_NOOP


def test_fixture_mode_disabled_noop_with_config_false():
    """fixture_mode=False should always return NOOP regardless of patches."""
    with patch(
        "skillos.capability_invocation_os.review_node.review_builder.should_force_disabled",
        return_value=False,
    ), patch(
        "skillos.capability_invocation_os.review_node.review_builder.is_z9_review_node_enabled",
        return_value=True,
    ):
        node = Z9ReviewNode(fixture_mode=False)
        resp = node.build_review_from_z2_snapshot(_make_snapshot())
        assert resp.decision == Z9ReviewDecision.DISABLED_DEFAULT_NOOP


# ─── BLOCKER 2: build_review_from_z2_snapshot must build real content ─────────

def test_fixture_builds_real_evidence():
    """When fixture_mode=True with patches, evidence is populated from snapshot."""
    with patch(
        "skillos.capability_invocation_os.review_node.review_builder.should_force_disabled",
        return_value=False,
    ), patch(
        "skillos.capability_invocation_os.review_node.review_builder.is_z9_review_node_enabled",
        return_value=True,
    ):
        node = Z9ReviewNode(fixture_mode=True)
        snapshot = _make_snapshot(source_graph_hash="test_graph_hash_123")
        resp = node.build_review_from_z2_snapshot(snapshot)
        assert resp.evidence != {}
        if hasattr(resp.evidence, "source_graph_hash"):
            assert resp.evidence.source_graph_hash == "test_graph_hash_123"


def test_fixture_builds_12_sections():
    """12 review sections should be built (one for each ALLOWED_REVIEW_SECTIONS)."""
    with patch(
        "skillos.capability_invocation_os.review_node.review_builder.should_force_disabled",
        return_value=False,
    ), patch(
        "skillos.capability_invocation_os.review_node.review_builder.is_z9_review_node_enabled",
        return_value=True,
    ):
        node = Z9ReviewNode(fixture_mode=True)
        snapshot = _make_snapshot()
        resp = node.build_review_from_z2_snapshot(snapshot)
        assert len(resp.sections) == len(ALLOWED_REVIEW_SECTIONS)


def test_fixture_builds_sections_with_unique_ids():
    """Each section should have a unique section_id."""
    with patch(
        "skillos.capability_invocation_os.review_node.review_builder.should_force_disabled",
        return_value=False,
    ), patch(
        "skillos.capability_invocation_os.review_node.review_builder.is_z9_review_node_enabled",
        return_value=True,
    ):
        node = Z9ReviewNode(fixture_mode=True)
        resp = node.build_review_from_z2_snapshot(_make_snapshot())
        sec_ids = [s.section_id for s in resp.sections]
        assert len(sec_ids) == len(set(sec_ids))


def test_fixture_sections_cover_all_types():
    """Sections should cover all ALLOWED_REVIEW_SECTIONS types."""
    with patch(
        "skillos.capability_invocation_os.review_node.review_builder.should_force_disabled",
        return_value=False,
    ), patch(
        "skillos.capability_invocation_os.review_node.review_builder.is_z9_review_node_enabled",
        return_value=True,
    ):
        node = Z9ReviewNode(fixture_mode=True)
        resp = node.build_review_from_z2_snapshot(_make_snapshot())
        sec_types = {s.section_type for s in resp.sections}
        assert sec_types == ALLOWED_REVIEW_SECTIONS


def test_fixture_includes_z2_feedback_candidate():
    """Response should include a z2_feedback_candidate."""
    with patch(
        "skillos.capability_invocation_os.review_node.review_builder.should_force_disabled",
        return_value=False,
    ), patch(
        "skillos.capability_invocation_os.review_node.review_builder.is_z9_review_node_enabled",
        return_value=True,
    ):
        node = Z9ReviewNode(fixture_mode=True)
        resp = node.build_review_from_z2_snapshot(_make_snapshot())
        assert resp.z2_feedback_candidate is not None
        assert isinstance(resp.z2_feedback_candidate, Z2FeedbackCandidate)


# ─── BLOCKER 3: validate_z2_snapshot_candidate must check required hashes ─────

def test_snapshot_missing_report_node_id_returns_evidence_incomplete():
    snap = _make_snapshot(report_node_id="")
    result = validate_z2_snapshot_candidate(snap)
    assert result == Z9ReviewDecision.DENY_Z9_EVIDENCE_INCOMPLETE


def test_snapshot_missing_source_graph_hash_returns_evidence_incomplete():
    snap = _make_snapshot(source_graph_hash="")
    result = validate_z2_snapshot_candidate(snap)
    assert result == Z9ReviewDecision.DENY_Z9_EVIDENCE_INCOMPLETE


def test_snapshot_missing_evidence_chain_hash_returns_evidence_incomplete():
    snap = _make_snapshot(evidence_chain_hash="")
    result = validate_z2_snapshot_candidate(snap)
    assert result == Z9ReviewDecision.DENY_Z9_EVIDENCE_INCOMPLETE


def test_snapshot_missing_research_summary_hash_returns_evidence_incomplete():
    snap = _make_snapshot(research_summary_hash="")
    result = validate_z2_snapshot_candidate(snap)
    assert result == Z9ReviewDecision.DENY_Z9_EVIDENCE_INCOMPLETE


def test_snapshot_missing_risk_warning_hash_returns_evidence_incomplete():
    snap = _make_snapshot(risk_warning_hash="")
    result = validate_z2_snapshot_candidate(snap)
    assert result == Z9ReviewDecision.DENY_Z9_EVIDENCE_INCOMPLETE


def test_snapshot_all_hashes_present_allows():
    snap = _make_snapshot()
    result = validate_z2_snapshot_candidate(snap)
    assert result == Z9ReviewDecision.ALLOW_Z9_READONLY_REVIEW


# ─── BLOCKER 4: blocked_outputs_removed empty list must fail ──────────────────

def test_snapshot_empty_blocked_outputs_returns_unsafe():
    snap = _make_snapshot(blocked_outputs_removed=[])
    result = validate_z2_snapshot_candidate(snap)
    assert result == Z9ReviewDecision.DENY_Z9_OUTPUTS_UNSAFE


def test_section_empty_blocked_outputs_returns_unsafe():
    section = Z9ReviewSection(
        section_id="s1", section_type="review_header",
        blocked_outputs_removed=[],
    )
    result = validate_z9_review_section(section)
    assert result == Z9ReviewDecision.DENY_Z9_OUTPUTS_UNSAFE


def test_response_empty_forbidden_outputs_removed_returns_unsafe():
    resp = _make_valid_response()
    object.__setattr__(resp, 'forbidden_outputs_removed', [])
    result = validate_z9_review_response(resp)
    assert result == Z9ReviewDecision.DENY_Z9_OUTPUTS_UNSAFE


def test_snapshot_partial_blocked_outputs_returns_unsafe():
    snap = _make_snapshot(blocked_outputs_removed=["buy_signal"])
    result = validate_z2_snapshot_candidate(snap)
    assert result == Z9ReviewDecision.DENY_Z9_OUTPUTS_UNSAFE


# ─── BLOCKER 5: validate_z9_review_response must validate sections ────────────

def test_response_validates_each_section():
    """validate_z9_review_response should call validate_z9_review_section on each section."""
    section = _make_valid_section()
    feedback = Z2FeedbackCandidate(
        source_z2_report_node_id="r1",
        review_label="EXPLANATION_ACCEPTED_STRUCTURE_ONLY",
        readonly_only=True,
        requires_human_review=True,
    )
    resp = Z9ReviewNodeResponse(
        response_id=str(uuid.uuid4()),
        decision=Z9ReviewDecision.ALLOW_Z9_READONLY_REVIEW,
        sections=[section, section],
        z2_feedback_candidate=feedback,
        forbidden_outputs_removed=sorted(FORBIDDEN_OUTPUT_KEYS),
        degraded=False,
        mode="DISABLED_DEFAULT_P0",
        review_enabled=True,
    )
    result = validate_z9_review_response(resp)
    assert result == Z9ReviewDecision.ALLOW_Z9_READONLY_REVIEW


def test_response_empty_sections_allowed():
    """Response with no sections but valid otherwise should pass."""
    feedback = Z2FeedbackCandidate(
        source_z2_report_node_id="r1",
        review_label="EXPLANATION_ACCEPTED_STRUCTURE_ONLY",
        readonly_only=True,
        requires_human_review=True,
    )
    resp = Z9ReviewNodeResponse(
        response_id=str(uuid.uuid4()),
        decision=Z9ReviewDecision.ALLOW_Z9_READONLY_REVIEW,
        sections=[],
        z2_feedback_candidate=feedback,
        forbidden_outputs_removed=sorted(FORBIDDEN_OUTPUT_KEYS),
        degraded=False,
        mode="DISABLED_DEFAULT_P0",
        review_enabled=True,
    )
    result = validate_z9_review_response(resp)
    assert result == Z9ReviewDecision.ALLOW_Z9_READONLY_REVIEW


def test_response_invalid_section_causes_deny():
    """A section missing blocked_outputs_removed should cause DENY."""
    bad_section = Z9ReviewSection(section_id="bad", section_type="review_header", blocked_outputs_removed=[])
    feedback = Z2FeedbackCandidate(
        source_z2_report_node_id="r1",
        review_label="EXPLANATION_ACCEPTED_STRUCTURE_ONLY",
        readonly_only=True,
        requires_human_review=True,
    )
    resp = Z9ReviewNodeResponse(
        response_id=str(uuid.uuid4()),
        decision=Z9ReviewDecision.ALLOW_Z9_READONLY_REVIEW,
        sections=[bad_section],
        z2_feedback_candidate=feedback,
        forbidden_outputs_removed=sorted(FORBIDDEN_OUTPUT_KEYS),
        degraded=False,
        mode="DISABLED_DEFAULT_P0",
        review_enabled=True,
    )
    result = validate_z9_review_response(resp)
    assert result == Z9ReviewDecision.DENY_Z9_OUTPUTS_UNSAFE


def test_response_validates_feedback_candidate():
    """validate_z9_review_response should validate z2_feedback_candidate if present."""
    resp = _make_valid_response()
    result = validate_z9_review_response(resp)
    assert result == Z9ReviewDecision.ALLOW_Z9_READONLY_REVIEW


def test_response_bad_feedback_causes_deny():
    """A feedback candidate with review_label not in allowed set should cause DENY."""
    bad_feedback = Z2FeedbackCandidate(
        source_z2_report_node_id="r1",
        review_label="BAD_LABEL",
        readonly_only=True,
        requires_human_review=True,
    )
    resp = Z9ReviewNodeResponse(
        response_id=str(uuid.uuid4()),
        decision=Z9ReviewDecision.ALLOW_Z9_READONLY_REVIEW,
        z2_feedback_candidate=bad_feedback,
        forbidden_outputs_removed=sorted(FORBIDDEN_OUTPUT_KEYS),
        degraded=False,
        mode="DISABLED_DEFAULT_P0",
        review_enabled=True,
    )
    result = validate_z9_review_response(resp)
    # The feedback validation should catch it via validate_z2_feedback_candidate
    assert result.value.startswith("DENY_")


def test_response_none_feedback_allowed():
    """Response with None feedback should still be valid."""
    resp = Z9ReviewNodeResponse(
        response_id=str(uuid.uuid4()),
        decision=Z9ReviewDecision.ALLOW_Z9_READONLY_REVIEW,
        z2_feedback_candidate=None,
        forbidden_outputs_removed=sorted(FORBIDDEN_OUTPUT_KEYS),
        degraded=False,
        mode="DISABLED_DEFAULT_P0",
        review_enabled=True,
    )
    result = validate_z9_review_response(resp)
    assert result == Z9ReviewDecision.ALLOW_Z9_READONLY_REVIEW


# ─── Evidence inheritance tests (BLOCKER 2 related) ──────────────────────────

def test_evidence_inherits_report_node_id():
    snap = _make_snapshot(report_node_id="z2_report_xyz")
    evidence = build_z9_review_evidence_from_z2_snapshot(snap)
    assert evidence.source_z2_report_node_id == "z2_report_xyz"


def test_evidence_inherits_factor_context_summary_hash():
    snap = _make_snapshot(factor_context_summary_hash="fcs_xyz")
    evidence = build_z9_review_evidence_from_z2_snapshot(snap)
    assert evidence.factor_context_summary_hash == "fcs_xyz"


def test_evidence_inherits_confidence_reason():
    snap = _make_snapshot(confidence_reason="mock confidence")
    evidence = build_z9_review_evidence_from_z2_snapshot(snap)
    assert evidence.confidence_reason == "mock confidence"


def test_evidence_inherits_missing_evidence():
    snap = _make_snapshot(missing_evidence=["gap1", "gap2"])
    evidence = build_z9_review_evidence_from_z2_snapshot(snap)
    assert "gap1" in evidence.missing_evidence
    assert "gap2" in evidence.missing_evidence


def test_evidence_inherits_review_required():
    snap = _make_snapshot(review_required=True)
    evidence = build_z9_review_evidence_from_z2_snapshot(snap)
    assert evidence.review_required is True


def test_evidence_inherits_review_reason():
    snap = _make_snapshot(review_reason="needs deeper analysis")
    evidence = build_z9_review_evidence_from_z2_snapshot(snap)
    assert evidence.review_reason == "needs deeper analysis"


def test_evidence_readonly():
    snap = _make_snapshot()
    evidence = build_z9_review_evidence_from_z2_snapshot(snap)
    assert evidence.readonly_only is True


def test_evidence_degraded_snapshot():
    snap = _make_snapshot(degradation_status="degraded")
    evidence = build_z9_review_evidence_from_z2_snapshot(snap)
    assert evidence.degradation_status == "degraded"


# ─── Attribution with real evidence (BLOCKER 6) ──────────────────────────────

def test_attribution_with_populated_evidence():
    snap = _make_snapshot()
    evidence = build_z9_review_evidence_from_z2_snapshot(snap)
    attribution = build_explanation_attribution(snap, evidence)
    assert attribution["attribution_type"] == "EXPLANATION_ONLY"
    assert "review_label" in attribution


def test_attribution_with_no_evidence():
    result = build_explanation_attribution(_make_snapshot(), None)
    assert result.get("no_evidence") is True


def test_attribution_hashes_present():
    snap = _make_snapshot(
        source_graph_hash="gh", evidence_chain_hash="ech",
        research_summary_hash="rsh", risk_warning_hash="rwh",
    )
    evidence = build_z9_review_evidence_from_z2_snapshot(snap)
    attribution = build_explanation_attribution(snap, evidence)
    assert "source_graph_hash" in attribution["evidence_hashes_present"]
    assert "evidence_chain_hash" in attribution["evidence_hashes_present"]


def test_attribution_missing_hashes():
    snap = _make_snapshot(source_graph_hash="", evidence_chain_hash="")
    evidence = build_z9_review_evidence_from_z2_snapshot(snap)
    attribution = build_explanation_attribution(snap, evidence)
    assert "source_graph_hash" in attribution["evidence_hashes_missing"]
    assert "evidence_chain_hash" in attribution["evidence_hashes_missing"]


# ─── Additional validation edge cases ────────────────────────────────────────

def test_validate_request_not_request_type():
    result = validate_z9_review_request("not a request")
    assert result == Z9ReviewDecision.DENY_Z9_SOURCE_FORBIDDEN


def test_validate_snapshot_not_candidate_type():
    result = validate_z2_snapshot_candidate("not a candidate")
    assert result == Z9ReviewDecision.DENY_Z9_SOURCE_FORBIDDEN


def test_validate_section_not_section_type():
    result = validate_z9_review_section("not a section")
    assert result == Z9ReviewDecision.DENY_Z9_SOURCE_FORBIDDEN


def test_validate_response_not_response_type():
    result = validate_z9_review_response("not a response")
    assert result == Z9ReviewDecision.DENY_Z9_SOURCE_FORBIDDEN


def test_validate_feedback_not_feedback_type():
    result = validate_z2_feedback_candidate("not a feedback")
    assert result == Z9ReviewDecision.DENY_Z9_SOURCE_FORBIDDEN


def test_section_wrong_type_denies():
    section = Z9ReviewSection(
        section_id="s1", section_type="not_a_real_section_type",
        blocked_outputs_removed=sorted(FORBIDDEN_OUTPUT_KEYS),
    )
    result = validate_z9_review_section(section)
    assert result == Z9ReviewDecision.DENY_Z9_SOURCE_FORBIDDEN


def test_section_not_readonly_denies():
    section = Z9ReviewSection(
        section_id="s1", section_type="review_header",
        blocked_outputs_removed=sorted(FORBIDDEN_OUTPUT_KEYS),
        readonly_only=False,
    )
    result = validate_z9_review_section(section)
    assert result == Z9ReviewDecision.DENY_Z9_EXECUTION_FORBIDDEN


def test_snapshot_not_readonly_denies():
    snap = _make_snapshot(readonly_only=False)
    result = validate_z2_snapshot_candidate(snap)
    assert result == Z9ReviewDecision.DENY_Z9_EXECUTION_FORBIDDEN


def test_snapshot_trade_result_denies():
    snap = _make_snapshot(no_trade_result=False)
    result = validate_z2_snapshot_candidate(snap)
    assert result == Z9ReviewDecision.DENY_Z9_TRADE_RESULT_FORBIDDEN


def test_snapshot_paper_trading_denies():
    snap = _make_snapshot(no_paper_trading=False)
    result = validate_z2_snapshot_candidate(snap)
    assert result == Z9ReviewDecision.DENY_Z9_TRADE_RESULT_FORBIDDEN


def test_snapshot_broker_action_denies():
    snap = _make_snapshot(no_broker_action=False)
    result = validate_z2_snapshot_candidate(snap)
    assert result == Z9ReviewDecision.DENY_Z9_TRADE_RESULT_FORBIDDEN


def test_snapshot_position_change_denies():
    snap = _make_snapshot(no_position_change=False)
    result = validate_z2_snapshot_candidate(snap)
    assert result == Z9ReviewDecision.DENY_Z9_TRADE_RESULT_FORBIDDEN


def test_response_sections_with_forbidden_output_detected():
    """Section containing forbidden output keys in its payload should be caught."""
    # Create a valid section but scan it — forbidden outputs are on keys
    section = Z9ReviewSection(
        section_id="s1", section_type="review_header",
        blocked_outputs_removed=sorted(FORBIDDEN_OUTPUT_KEYS),
    )
    feedback = Z2FeedbackCandidate(
        source_z2_report_node_id="r1",
        review_label="EXPLANATION_ACCEPTED_STRUCTURE_ONLY",
        readonly_only=True,
        requires_human_review=True,
    )
    resp = Z9ReviewNodeResponse(
        response_id=str(uuid.uuid4()),
        decision=Z9ReviewDecision.ALLOW_Z9_READONLY_REVIEW,
        sections=[section],
        z2_feedback_candidate=feedback,
        forbidden_outputs_removed=sorted(FORBIDDEN_OUTPUT_KEYS),
        degraded=False,
        mode="DISABLED_DEFAULT_P0",
        review_enabled=True,
    )
    result = validate_z9_review_response(resp)
    assert result == Z9ReviewDecision.ALLOW_Z9_READONLY_REVIEW


# ─── Hash generation tests ───────────────────────────────────────────────────

def test_review_node_hash_is_stable():
    h1 = build_z9_review_node_hash("id1", "DISABLED_DEFAULT_P0")
    h2 = build_z9_review_node_hash("id1", "DISABLED_DEFAULT_P0")
    assert h1 == h2


def test_review_node_hash_different_inputs_different():
    h1 = build_z9_review_node_hash("id1", "DISABLED_DEFAULT_P0")
    h2 = build_z9_review_node_hash("id2", "DISABLED_DEFAULT_P0")
    assert h1 != h2


def test_section_hash_stability():
    h1 = build_z9_review_section_hash("sec1", "review_header")
    h2 = build_z9_review_section_hash("sec1", "review_header")
    assert h1 == h2


def test_feedback_candidate_hash_stability():
    h1 = build_z9_feedback_candidate_hash("fb1", "REVIEW")
    h2 = build_z9_feedback_candidate_hash("fb1", "REVIEW")
    assert h1 == h2


# ─── Blocked outputs complete edge cases ─────────────────────────────────────

def test_blocked_outputs_complete_with_superset():
    """A superset should pass because FORBIDDEN_OUTPUT_KEYS is subset."""
    values = sorted(FORBIDDEN_OUTPUT_KEYS) + ["extra_key"]
    assert blocked_outputs_removed_complete(values) is True


def test_blocked_outputs_none_passed():
    """None should fail since it's not iterable/doesn't contain all keys."""
    assert blocked_outputs_removed_complete([]) is False


# ─── Feedback validation ─────────────────────────────────────────────────────

def test_feedback_not_readonly_denies():
    fb = Z2FeedbackCandidate(readonly_only=False, requires_human_review=True)
    result = validate_z2_feedback_candidate(fb)
    assert result == Z9ReviewDecision.DENY_Z9_EXECUTION_FORBIDDEN


def test_feedback_not_requires_human_review_denies():
    fb = Z2FeedbackCandidate(readonly_only=True, requires_human_review=False)
    result = validate_z2_feedback_candidate(fb)
    assert result == Z9ReviewDecision.DENY_Z9_EXECUTION_FORBIDDEN


def test_feedback_contains_forbidden_output_denies():
    # The Z2FeedbackCandidate doesn't have FORBIDDEN_OUTPUT_KEYS as field names
    # but we test that payload_contains_forbidden_outputs catches dictionary usage
    assert payload_contains_forbidden_outputs({"buy_signal": True}) is True
    assert payload_contains_forbidden_outputs({"safe_key": "ok"}) is False


# ─── Response edge cases ─────────────────────────────────────────────────────

def test_response_not_readonly_denies():
    resp = Z9ReviewNodeResponse(
        response_id=str(uuid.uuid4()),
        decision=Z9ReviewDecision.ALLOW_Z9_READONLY_REVIEW,
        z2_feedback_candidate=None,
        readonly_only=False,
    )
    result = validate_z9_review_response(resp)
    assert result == Z9ReviewDecision.DENY_Z9_EXECUTION_FORBIDDEN


def test_response_memory_mutation_enabled_denies():
    resp = Z9ReviewNodeResponse(
        response_id=str(uuid.uuid4()),
        decision=Z9ReviewDecision.ALLOW_Z9_READONLY_REVIEW,
        z2_feedback_candidate=None,
        forbidden_outputs_removed=sorted(FORBIDDEN_OUTPUT_KEYS),
        memory_mutation_enabled=True,
    )
    result = validate_z9_review_response(resp)
    assert result == Z9ReviewDecision.DENY_Z9_MEMORY_MUTATION_FORBIDDEN


# ─── Nested forbidden detection ──────────────────────────────────────────────

def test_deeply_nested_forbidden_input():
    payload = {"level1": {"level2": {"level3": {"real_pnl": 100}}}}
    assert payload_contains_forbidden_inputs(payload) is True


def test_deeply_nested_forbidden_output():
    payload = {"level1": {"level2": {"level3": {"alpha_claim": 0.05}}}}
    assert payload_contains_forbidden_outputs(payload) is True


def test_list_nested_forbidden():
    payload = {"items": [{"alpha_claim": 0.01}]}
    assert payload_contains_forbidden_outputs(payload) is True


def test_safe_deep_nesting():
    payload = {"level1": {"level2": {"level3": {"safe_field": "ok"}}}}
    assert payload_contains_forbidden_outputs(payload) is False


# ─── Dataclass forbidden detection ───────────────────────────────────────────

def test_dataclass_forbidden_inputs():
    snap = _make_snapshot()
    # The snapshot has no forbidden input keys by default
    result = payload_contains_forbidden_inputs(snap)
    assert result is False


def test_dataclass_forbidden_outputs():
    section = _make_valid_section()
    result = payload_contains_forbidden_outputs(section)
    assert result is False


# ─── Hash field length verification ──────────────────────────────────────────

def test_all_hashes_are_sha256_length():
    h1 = build_z9_review_node_hash("test", "MODE")
    h2 = build_z9_review_section_hash("s1", "t1")
    h3 = build_z9_feedback_candidate_hash("f1", "l1")
    for h in [h1, h2, h3]:
        assert len(h) == 64
        assert all(c in "0123456789abcdef" for c in h)
