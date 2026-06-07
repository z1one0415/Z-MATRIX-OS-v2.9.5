"""Deny-by-default router — disabled returns DENY_NOOP."""
from skillos.capability_invocation_os.runtime.models import InvocationRequest, InvocationDecision

def route(request: InvocationRequest) -> InvocationDecision:
    return InvocationDecision(action="DENY", reason="router disabled by default", evidence_required=True)
