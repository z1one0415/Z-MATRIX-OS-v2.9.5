"""Contracts — disabled-default, no real validation in P0. Returns deny decisions."""
from skillos.capability_invocation_os.adapters.factor_library.constants import (
    CANONICAL_READONLY_INTENTS, FORBIDDEN_INTENTS, BLOCKED_OUTPUTS,
)
from skillos.capability_invocation_os.adapters.factor_library.models import (
    FactorAdapterDecision, FactorApplicationContractView, FactorInvocationRequest, FactorInvocationResponse,
)
from skillos.capability_invocation_os.adapters.factor_library.degradation import disabled_default_noop, deny_execution_forbidden

def validate_readonly_intent(intent: str) -> bool:
    return intent in CANONICAL_READONLY_INTENTS

def validate_forbidden_intent(intent: str) -> bool:
    return intent in FORBIDDEN_INTENTS

def validate_application_contract_view(contract: FactorApplicationContractView) -> FactorAdapterDecision:
    if not contract.execution_requested:
        for mode in contract.blocked_application_modes:
            if mode in FORBIDDEN_INTENTS:
                return deny_execution_forbidden()
    return disabled_default_noop()

def validate_invocation_request(request: FactorInvocationRequest) -> FactorAdapterDecision:
    if request.execution_requested:
        return deny_execution_forbidden()
    if request.intent in FORBIDDEN_INTENTS:
        return deny_execution_forbidden()
    return disabled_default_noop()

def validate_blocked_outputs_removed(response: FactorInvocationResponse) -> FactorAdapterDecision:
    missing = [o for o in BLOCKED_OUTPUTS if o not in getattr(response, 'forbidden_outputs_removed', [])]
    if missing:
        return deny_execution_forbidden()
    return disabled_default_noop()
