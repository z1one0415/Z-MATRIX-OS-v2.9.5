"""No-op composition validator — multi-skill chains disabled."""
from skillos.capability_invocation_os.runtime.models import InvocationRequest, InvocationDecision

def validate_chain(requests: list) -> InvocationDecision:
    if len(requests) > 1:
        return InvocationDecision(action="DENY", reason="composition disabled by default")
    return InvocationDecision(action="DENY", reason="composition disabled by default")
