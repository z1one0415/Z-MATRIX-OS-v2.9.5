"""Tests for Z9 models."""
from skillos.capability_invocation_os.review_node.models import (
    Z9ReviewNodeResponse, Z9ReviewNodeRequest, Z9ReviewSection,
    Z9ReviewEvidence, Z9ReviewDecision, Z2FeedbackCandidate, Z9ReviewDegradationStatus,
)
from skillos.capability_invocation_os.review_node.constants import FORBIDDEN_OUTPUT_KEYS

def test_response_defaults_safe():
    r = Z9ReviewNodeResponse()
    assert r.readonly_only is True
    assert r.no_trade_result is True
    assert r.no_paper_trading is True
    assert r.no_broker_action is True
    assert r.no_position_change is True
    assert r.memory_mutation_enabled is False

def test_response_forbidden_outputs_removed():
    r = Z9ReviewNodeResponse()
    for key in FORBIDDEN_OUTPUT_KEYS:
        assert key in r.forbidden_outputs_removed

def test_request_defaults():
    r = Z9ReviewNodeRequest()
    assert r.execution_requested is False
    assert r.memory_mutation_requested is False

def test_section_defaults():
    s = Z9ReviewSection()
    assert s.readonly_only is True

def test_evidence_defaults():
    e = Z9ReviewEvidence()
    assert e.readonly_only is True
    assert e.privacy_marker is True

def test_feedback_defaults():
    f = Z2FeedbackCandidate()
    assert f.readonly_only is True
    assert f.requires_human_review is True

def test_no_forbidden_fields_in_response():
    r = Z9ReviewNodeResponse()
    forbidden = {"trade_instruction","buy_signal","sell_signal","position_weight","order_signal","real_pnl","alpha_claim","memory_mutation_result","persistent_memory_write"}
    for f in forbidden:
        assert not hasattr(r, f), f"Response should not have attribute: {f}"
