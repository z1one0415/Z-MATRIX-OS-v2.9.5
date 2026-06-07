"""Contract validation skeleton — disabled default returns DENY_CONTINUE."""
from skillos.capability_invocation_os.runtime.models import InvocationRequest, CapabilityContract, InvocationDecision

def validate(request: InvocationRequest, contract: CapabilityContract) -> InvocationDecision:
    return InvocationDecision(action="DENY", reason="validation disabled by default", evidence_required=True)
