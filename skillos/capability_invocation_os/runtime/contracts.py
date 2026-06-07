"""Contract validation — disabled default returns DENY_NOOP/NEEDS_HUMAN_REVIEW."""
from skillos.capability_invocation_os.runtime.models import InvocationRequest, CapabilityContract, InvocationDecision, ValidationResult
from skillos.capability_invocation_os.runtime.validation import validate_contract_shape, validate_no_execution_fields

def validate_input_schema(request, contract):
    if not hasattr(request,"inputs"): return InvocationDecision(action="DENY_NOOP", reason="no inputs", evidence_required=True)
    return InvocationDecision(action="NEEDS_HUMAN_REVIEW", reason="input validation disabled", evidence_required=True)

def validate_output_schema_placeholder(contract):
    return InvocationDecision(action="NEEDS_HUMAN_REVIEW", reason="output validation disabled", evidence_required=True)

def validate_side_effect_declaration(contract):
    return InvocationDecision(action="NEEDS_HUMAN_REVIEW", reason="side-effect validation disabled", evidence_required=True)

def validate_forbidden_actions(contract):
    v = validate_no_execution_fields(contract)
    if not v.valid: return InvocationDecision(action="DENY", reason=f"forbidden: {v.errors}", evidence_required=True)
    return InvocationDecision(action="NEEDS_HUMAN_REVIEW", reason="forbidden action validation disabled", evidence_required=True)

def validate_contract(request, contract):
    shape = validate_contract_shape(contract)
    if not shape.valid: return InvocationDecision(action="DENY_NOOP", reason=f"invalid contract: {shape.errors}", evidence_required=True)
    return InvocationDecision(action="NEEDS_HUMAN_REVIEW", reason="contract validation disabled by default", evidence_required=True)
