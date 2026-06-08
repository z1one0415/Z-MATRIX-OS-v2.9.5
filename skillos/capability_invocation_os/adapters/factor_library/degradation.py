"""Degradation — all DENY builders return structured objects. No raise. No block."""
from dataclasses import dataclass
from skillos.capability_invocation_os.adapters.factor_library.models import FactorAdapterDecision, FactorInvocationResponse

@dataclass
class DegradedResponse:
    decision: FactorAdapterDecision
    degraded: bool = True
    mode: str = "PLAN_ONLY"

def deny_factor_not_found() -> FactorAdapterDecision:
    return FactorAdapterDecision.DENY_FACTOR_NOT_FOUND

def deny_factor_not_validated() -> FactorAdapterDecision:
    return FactorAdapterDecision.DENY_FACTOR_NOT_VALIDATED

def deny_pit_failed() -> FactorAdapterDecision:
    return FactorAdapterDecision.DENY_PIT_FAILED

def deny_coverage_failed() -> FactorAdapterDecision:
    return FactorAdapterDecision.DENY_COVERAGE_FAILED

def deny_family_overlap() -> FactorAdapterDecision:
    return FactorAdapterDecision.DENY_FAMILY_OVERLAP

def deny_guardrail_failed() -> FactorAdapterDecision:
    return FactorAdapterDecision.DENY_GUARDRAIL_FAILED

def deny_promotion_not_allowed() -> FactorAdapterDecision:
    return FactorAdapterDecision.DENY_PROMOTION_NOT_ALLOWED

def deny_execution_forbidden() -> FactorAdapterDecision:
    return FactorAdapterDecision.DENY_EXECUTION_FORBIDDEN

def disabled_default_noop() -> FactorAdapterDecision:
    return FactorAdapterDecision.DISABLED_DEFAULT_NOOP
