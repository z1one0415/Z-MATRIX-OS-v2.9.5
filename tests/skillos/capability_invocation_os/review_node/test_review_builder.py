"""Tests for Z9 review builder."""
from skillos.capability_invocation_os.review_node.models import Z9ReviewNodeResponse, Z9ReviewDecision
from skillos.capability_invocation_os.review_node.review_builder import Z9ReviewNode

def test_default_returns_disabled_noop():
    node = Z9ReviewNode()
    resp = node.build_disabled_default_response()
    assert resp.decision.value == "DISABLED_DEFAULT_NOOP"

def test_fixture_mode_false_noop():
    node = Z9ReviewNode(fixture_mode=False)
    resp = node.build_review_from_z2_snapshot(None)
    assert resp.decision.value == "DISABLED_DEFAULT_NOOP"

def test_degraded_response():
    node = Z9ReviewNode()
    resp = node.build_degraded_review(Z9ReviewDecision.DENY_Z9_SOURCE_FORBIDDEN)
    assert resp.degraded is True
    assert resp.readonly_only is True

def test_forbidden_outputs_blocked():
    node = Z9ReviewNode()
    resp = node.build_disabled_default_response()
    assert "alpha_claim" in resp.forbidden_outputs_removed
    assert "trade_result" in resp.forbidden_outputs_removed
    assert "real_pnl" in resp.forbidden_outputs_removed
    assert "buy_signal" in resp.forbidden_outputs_removed
    assert "sell_signal" in resp.forbidden_outputs_removed
    assert "position_weight" in resp.forbidden_outputs_removed
