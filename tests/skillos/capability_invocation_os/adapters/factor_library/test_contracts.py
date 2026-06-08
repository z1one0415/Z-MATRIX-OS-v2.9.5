import pytest
from skillos.capability_invocation_os.adapters.factor_library.contracts import (
    validate_readonly_intent, validate_forbidden_intent, validate_invocation_request,
)
from skillos.capability_invocation_os.adapters.factor_library.models import FactorInvocationRequest, FactorAdapterDecision

def test_canonical_readonly_accepted():
    assert validate_readonly_intent("REGISTRY_READ") is True
    assert validate_readonly_intent("EVIDENCE_READ") is True

def test_forbidden_intents_flagged():
    assert validate_forbidden_intent("ALPHA_SIGNAL") is True
    assert validate_forbidden_intent("BROKER_RUNTIME") is True

def test_execution_requested_denied():
    req = FactorInvocationRequest(execution_requested=True)
    decision = validate_invocation_request(req)
    assert decision == FactorAdapterDecision.DENY_EXECUTION_FORBIDDEN
