import pytest
from skillos.capability_invocation_os.adapters.factor_library.models import (
    FactorInvocationRequest, FactorInvocationResponse, FactorAdapterDecision,
    FactorValidationSnapshotView, FactorApplicationContractView,
)

def test_defaults_safe():
    req = FactorInvocationRequest()
    assert req.execution_requested is False

def test_production_broker_blocked():
    c = FactorApplicationContractView()
    assert "PRODUCTION" in c.blocked_application_modes
    assert "BROKER_RUNTIME" in c.blocked_application_modes
    assert "REAL_TRADE" in c.blocked_application_modes

def test_alpha_claim_promotion_false():
    v = FactorValidationSnapshotView()
    assert v.promotion_allowed is False
    assert v.alpha_claim_allowed is False

def test_response_has_forbidden_outputs():
    resp = FactorInvocationResponse()
    assert len(resp.forbidden_outputs_removed) > 0

def test_decision_enum_values():
    assert "DENY_EXECUTION_FORBIDDEN" in FactorAdapterDecision._value2member_map_
    assert "DISABLED_DEFAULT_NOOP" in FactorAdapterDecision._value2member_map_
