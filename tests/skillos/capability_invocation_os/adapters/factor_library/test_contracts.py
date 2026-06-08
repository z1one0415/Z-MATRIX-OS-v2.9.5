"""Contract tests — verify validation semantics: complete blocks OK, missing blocks denied."""
import pytest
from skillos.capability_invocation_os.adapters.factor_library.contracts import (
    validate_readonly_intent, validate_forbidden_intent,
    validate_application_contract_view, validate_invocation_request,
    validate_blocked_outputs_removed,
)
from skillos.capability_invocation_os.adapters.factor_library.models import (
    FactorInvocationRequest, FactorInvocationResponse, FactorAdapterDecision,
    FactorApplicationContractView,
)
from skillos.capability_invocation_os.adapters.factor_library.constants import (
    FORBIDDEN_INTENTS, BLOCKED_OUTPUTS, CANONICAL_READONLY_INTENTS,
)


def test_canonical_readonly_accepted():
    assert validate_readonly_intent("REGISTRY_READ") is True
    assert validate_readonly_intent("EVIDENCE_READ") is True
    assert validate_readonly_intent("COMPOSITION_GRAPH_DRY_PLAN") is True


def test_forbidden_intents_flagged():
    assert validate_forbidden_intent("ALPHA_SIGNAL") is True
    assert validate_forbidden_intent("BROKER_RUNTIME") is True


def test_unknown_intent_not_readonly():
    assert validate_readonly_intent("UNKNOWN_INTENT") is False


def test_unknown_intent_not_forbidden():
    assert validate_forbidden_intent("UNKNOWN_INTENT") is False


def test_valid_contract_complete_block_lists_returns_disabled_noop():
    contract = FactorApplicationContractView()  # defaults: all blocked, no execution
    decision = validate_application_contract_view(contract)
    assert decision == FactorAdapterDecision.DISABLED_DEFAULT_NOOP


def test_contract_missing_blocked_mode_denied():
    modes = list(FORBIDDEN_INTENTS)
    modes.remove("ALPHA_SIGNAL")
    contract = FactorApplicationContractView(blocked_application_modes=modes)
    decision = validate_application_contract_view(contract)
    assert decision == FactorAdapterDecision.DENY_EXECUTION_FORBIDDEN


def test_contract_missing_blocked_output_denied():
    outputs = list(BLOCKED_OUTPUTS)
    outputs.remove("alpha_claim")
    contract = FactorApplicationContractView(blocked_outputs=outputs)
    decision = validate_application_contract_view(contract)
    assert decision == FactorAdapterDecision.DENY_EXECUTION_FORBIDDEN


def test_contract_execution_requested_denied():
    contract = FactorApplicationContractView(execution_requested=True)
    decision = validate_application_contract_view(contract)
    assert decision == FactorAdapterDecision.DENY_EXECUTION_FORBIDDEN


def test_contract_alpha_allowed_denied():
    contract = FactorApplicationContractView(alpha_claim_allowed=True)
    decision = validate_application_contract_view(contract)
    assert decision == FactorAdapterDecision.DENY_EXECUTION_FORBIDDEN


def test_invocation_unknown_intent_denied():
    req = FactorInvocationRequest(intent="UNKNOWN_INTENT")
    decision = validate_invocation_request(req)
    assert decision == FactorAdapterDecision.DENY_EXECUTION_FORBIDDEN


def test_invocation_forbidden_intent_denied():
    req = FactorInvocationRequest(intent="ALPHA_SIGNAL")
    decision = validate_invocation_request(req)
    assert decision == FactorAdapterDecision.DENY_EXECUTION_FORBIDDEN


def test_invocation_execution_requested_denied():
    req = FactorInvocationRequest(intent="REGISTRY_READ", execution_requested=True)
    decision = validate_invocation_request(req)
    assert decision == FactorAdapterDecision.DENY_EXECUTION_FORBIDDEN


def test_invocation_readonly_returns_disabled_noop():
    req = FactorInvocationRequest(intent="REGISTRY_READ", execution_requested=False)
    decision = validate_invocation_request(req)
    assert decision == FactorAdapterDecision.DISABLED_DEFAULT_NOOP


def test_blocked_outputs_complete_returns_disabled_noop():
    resp = FactorInvocationResponse(forbidden_outputs_removed=list(BLOCKED_OUTPUTS))
    decision = validate_blocked_outputs_removed(resp)
    assert decision == FactorAdapterDecision.DISABLED_DEFAULT_NOOP


def test_blocked_outputs_missing_alpha_denied():
    outputs = [o for o in BLOCKED_OUTPUTS if o != "alpha_claim"]
    resp = FactorInvocationResponse(forbidden_outputs_removed=outputs)
    decision = validate_blocked_outputs_removed(resp)
    assert decision == FactorAdapterDecision.DENY_EXECUTION_FORBIDDEN


def test_all_forbidden_intents_blocked_in_default_contract():
    contract = FactorApplicationContractView()
    for intent in FORBIDDEN_INTENTS:
        assert intent in contract.blocked_application_modes, f"{intent} not blocked"


def test_all_blocked_outputs_present_in_default_contract():
    contract = FactorApplicationContractView()
    for out in BLOCKED_OUTPUTS:
        assert out in contract.blocked_outputs, f"{out} missing"
