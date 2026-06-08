"""Contracts — disabled-default, no real validation in P0. Returns deny decisions."""

from skillos.capability_invocation_os.adapters.factor_library.constants import (
    CANONICAL_READONLY_INTENTS, FORBIDDEN_INTENTS, BLOCKED_OUTPUTS,
)
from skillos.capability_invocation_os.adapters.factor_library.models import (
    FactorAdapterDecision, FactorApplicationContractView, FactorInvocationRequest,
    FactorInvocationResponse,
)
from skillos.capability_invocation_os.adapters.factor_library.degradation import (
    disabled_default_noop, deny_execution_forbidden,
)


def validate_readonly_intent(intent: str) -> bool:
    """Return True if intent is a canonical readonly intent. Forbidden/unknown -> False."""
    return intent in CANONICAL_READONLY_INTENTS


def validate_forbidden_intent(intent: str) -> bool:
    """Return True if intent is in the forbidden set. Readonly/unknown -> False."""
    return intent in FORBIDDEN_INTENTS


def validate_application_contract_view(contract: FactorApplicationContractView) -> FactorAdapterDecision:
    """Validate contract semantics.
    Complete blocked configuration -> DISABLED_DEFAULT_NOOP.
    Missing blocked items, execution requested, or alpha_allowed -> DENY."""
    if contract.execution_requested:
        return deny_execution_forbidden()
    # Check all forbidden modes are blocked
    for mode in FORBIDDEN_INTENTS:
        if mode not in contract.blocked_application_modes:
            return deny_execution_forbidden()
    # Check all blocked outputs are present
    for out in BLOCKED_OUTPUTS:
        if out not in contract.blocked_outputs:
            return deny_execution_forbidden()
    if contract.alpha_claim_allowed:
        return deny_execution_forbidden()
    if contract.promotion_allowed:
        return deny_execution_forbidden()
    return disabled_default_noop()


def validate_invocation_request(request: FactorInvocationRequest) -> FactorAdapterDecision:
    """Validate a factor invocation request.
    Execution requested, forbidden intent, or unknown intent -> DENY.
    Readonly intent -> DISABLED_DEFAULT_NOOP."""
    if request.execution_requested:
        return deny_execution_forbidden()
    if request.intent in FORBIDDEN_INTENTS:
        return deny_execution_forbidden()
    if request.intent not in CANONICAL_READONLY_INTENTS:
        return deny_execution_forbidden()
    return disabled_default_noop()


def validate_blocked_outputs_removed(response: FactorInvocationResponse) -> FactorAdapterDecision:
    """Validate that all required outputs are blocked.
    If any BLOCKED_OUTPUT is missing from forbidden_outputs_removed -> DENY.
    Complete coverage -> DISABLED_DEFAULT_NOOP."""
    missing = [o for o in BLOCKED_OUTPUTS
               if o not in getattr(response, 'forbidden_outputs_removed', [])]
    if missing:
        return deny_execution_forbidden()
    return disabled_default_noop()
