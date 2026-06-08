import pytest
from skillos.capability_invocation_os.adapters.factor_library.degradation import (
    deny_factor_not_found, deny_factor_not_validated, deny_pit_failed,
    deny_coverage_failed, deny_family_overlap, deny_guardrail_failed,
    deny_promotion_not_allowed, deny_execution_forbidden, disabled_default_noop,
)
from skillos.capability_invocation_os.adapters.factor_library.models import FactorAdapterDecision

def test_all_deny_builders_return_decision():
    assert deny_factor_not_found() == FactorAdapterDecision.DENY_FACTOR_NOT_FOUND
    assert deny_factor_not_validated() == FactorAdapterDecision.DENY_FACTOR_NOT_VALIDATED
    assert deny_pit_failed() == FactorAdapterDecision.DENY_PIT_FAILED
    assert deny_coverage_failed() == FactorAdapterDecision.DENY_COVERAGE_FAILED
    assert deny_family_overlap() == FactorAdapterDecision.DENY_FAMILY_OVERLAP
    assert deny_guardrail_failed() == FactorAdapterDecision.DENY_GUARDRAIL_FAILED
    assert deny_promotion_not_allowed() == FactorAdapterDecision.DENY_PROMOTION_NOT_ALLOWED
    assert deny_execution_forbidden() == FactorAdapterDecision.DENY_EXECUTION_FORBIDDEN

def test_deny_builders_no_raise():
    try:
        deny_factor_not_found()
        deny_execution_forbidden()
        disabled_default_noop()
    except: pytest.fail("Deny builder raised")

def test_disabled_default_noop():
    assert disabled_default_noop() == FactorAdapterDecision.DISABLED_DEFAULT_NOOP
