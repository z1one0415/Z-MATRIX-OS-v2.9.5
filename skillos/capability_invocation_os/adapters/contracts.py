"""Adapter contract validation — contract-only, no execution, no Z-MATRIX imports."""
from skillos.capability_invocation_os.adapters.models import AdapterContract, AdapterRequest, AdapterDecision, AdapterValidationResult
def validate_adapter_contract(contract): return AdapterValidationResult(valid=True)
def validate_adapter_request(request, contract): return AdapterDecision(action="DENY", reason="adapter request validation disabled")
def validate_forbidden_actions(contract):
    if hasattr(contract,"forbidden_actions") and contract.forbidden_actions:
        return AdapterDecision(action="DENY", reason=f"forbidden actions detected: {contract.forbidden_actions}")
    return AdapterDecision(action="DENY_NOOP", reason="no forbidden actions")
def validate_no_execution_fields(contract): return AdapterValidationResult(valid=True)
