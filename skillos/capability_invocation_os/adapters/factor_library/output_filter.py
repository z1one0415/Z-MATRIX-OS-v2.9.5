"""Output filter — removes all forbidden fields. No mutation. Returns copy."""
from copy import deepcopy
from skillos.capability_invocation_os.adapters.factor_library.constants import BLOCKED_OUTPUTS
from skillos.capability_invocation_os.adapters.factor_library.models import FactorAdapterDecision

def remove_forbidden_outputs(payload: dict) -> dict:
    cleaned = {}
    for k, v in payload.items():
        if k not in BLOCKED_OUTPUTS:
            cleaned[k] = deepcopy(v)
    return cleaned

def list_removed_forbidden_outputs(payload: dict) -> list:
    return [k for k in payload if k in BLOCKED_OUTPUTS]

def assert_no_forbidden_outputs(payload: dict) -> FactorAdapterDecision:
    if any(k in BLOCKED_OUTPUTS for k in payload):
        from skillos.capability_invocation_os.adapters.factor_library.degradation import deny_execution_forbidden
        return deny_execution_forbidden()
    from skillos.capability_invocation_os.adapters.factor_library.degradation import disabled_default_noop
    return disabled_default_noop()
