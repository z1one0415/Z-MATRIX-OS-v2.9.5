"""Tests for Z9 contracts."""
from skillos.capability_invocation_os.review_node.models import (
    Z9ReviewDecision, Z9ReviewNodeRequest, Z9ReviewNodeResponse, Z9ReviewSection, Z2FeedbackCandidate,
)
from skillos.capability_invocation_os.review_node.contracts import (
    validate_z9_review_request, validate_z2_snapshot_candidate, validate_z9_review_section,
    validate_z9_review_response, validate_z2_feedback_candidate,
    payload_contains_forbidden_inputs, payload_contains_forbidden_outputs,
    blocked_outputs_removed_complete,
)
from skillos.capability_invocation_os.review_node.constants import FORBIDDEN_OUTPUT_KEYS

def test_execution_requested_denied():
    req = Z9ReviewNodeRequest(request_id="test", execution_requested=True)
    result = validate_z9_review_request(req)
    assert result == Z9ReviewDecision.DENY_Z9_EXECUTION_FORBIDDEN

def test_valid_request_allowed():
    req = Z9ReviewNodeRequest()
    result = validate_z9_review_request(req)
    assert result == Z9ReviewDecision.ALLOW_Z9_READONLY_REVIEW

def test_memory_mutation_requested_denied():
    req = Z9ReviewNodeRequest(request_id="test", memory_mutation_requested=True)
    result = validate_z9_review_request(req)
    assert result == Z9ReviewDecision.DENY_Z9_MEMORY_MUTATION_FORBIDDEN

def test_forbidden_input_detection():
    assert payload_contains_forbidden_inputs({"trade_result": 0.5}) is True
    assert payload_contains_forbidden_inputs({"real_pnl": 100}) is True
    assert payload_contains_forbidden_inputs({"safe_field": "ok"}) is False

def test_forbidden_output_detection():
    assert payload_contains_forbidden_outputs({"alpha_claim": 0.05}) is True
    assert payload_contains_forbidden_outputs({"buy_signal": True}) is True
    assert payload_contains_forbidden_outputs({"safe": "ok"}) is False

def test_nested_forbidden_detection():
    payload = {"nested": {"alpha_claim": 0.05}}
    assert payload_contains_forbidden_outputs(payload) is True

def test_blocked_outputs_complete():
    assert blocked_outputs_removed_complete(sorted(FORBIDDEN_OUTPUT_KEYS)) is True
    assert blocked_outputs_removed_complete(["buy_signal", "sell_signal"]) is False

def test_z9_section_valid():
    section = Z9ReviewSection(section_id="s1", section_type="review_header")
    result = validate_z9_review_section(section)
    assert result == Z9ReviewDecision.ALLOW_Z9_READONLY_REVIEW

def test_feedback_readonly():
    f = Z2FeedbackCandidate()
    result = validate_z2_feedback_candidate(f)
    assert result == Z9ReviewDecision.ALLOW_Z9_READONLY_REVIEW
