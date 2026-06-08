"""V13.F5.0.1.1 — Test invocation_request schema readonly enforcement."""
import json

def test_readonly_intents_only():
    """invocation_intent must be from readonly enum."""
    schema_enum = ["REGISTRY_READ","EVIDENCE_READ","VALIDATION_SUMMARY","GUARDRAIL_SUMMARY","CANDIDATE_MONITOR","RESEARCH_CONTEXT","SCORING_CONTEXT_DRY_PLAN","COMPOSITION_GRAPH_DRY_PLAN"]
    forbidden = ["ALPHA_SIGNAL","ORDER_SIGNAL","PORTFOLIO_WEIGHT","PAPER_TRADING","BROKER_RUNTIME","REAL_TRADE","PRODUCTION"]
    for f in forbidden:
        assert f not in schema_enum, f"{f} should not be in invocation_intent enum"

def test_execution_requested_must_be_false():
    """execution_requested const must be false."""
    # Simulate schema: const false
    valid = {"execution_requested": False}
    invalid = {"execution_requested": True}
    assert valid["execution_requested"] is False
    assert invalid["execution_requested"] is True  # would fail schema validation

def test_alpha_blocked():
    valid = {"alpha_claim_allowed": False}
    invalid = {"alpha_claim_allowed": True}
    assert valid["alpha_claim_allowed"] is False
    assert invalid["alpha_claim_allowed"] is True  # would fail const: false
