"""Shape and safety validation — no execution, no adapter import."""
from skillos.capability_invocation_os.runtime.constants import FORBIDDEN_MODULES, CAPABILITY_TAGS
from skillos.capability_invocation_os.runtime.models import ValidationResult

def validate_no_forbidden_modules(text_or_names):
    if isinstance(text_or_names, str): text_or_names = [text_or_names]
    hits = [n for n in text_or_names if n.lower() in FORBIDDEN_MODULES]
    return ValidationResult(valid=len(hits)==0, errors=hits, severity="DENY" if hits else "CONTINUE")

def validate_no_execution_fields(contract):
    if hasattr(contract, "forbidden_actions"):
        exec_hits = [a for a in contract.forbidden_actions if any(t in a.lower() for t in CAPABILITY_TAGS)]
        return ValidationResult(valid=len(exec_hits)==0, errors=exec_hits, severity="DENY" if exec_hits else "CONTINUE")
    return ValidationResult(valid=True)

def validate_contract_shape(contract):
    required = ["skill_id", "risk_tier", "permission_required"]
    missing = [r for r in required if not hasattr(contract, r)]
    return ValidationResult(valid=len(missing)==0, errors=missing, severity="DENY_NOOP" if missing else "CONTINUE")

def validate_request_shape(request):
    if not hasattr(request, "capability_id"): return ValidationResult(valid=False, errors=["missing capability_id"], severity="DENY_NOOP")
    return ValidationResult(valid=True)
