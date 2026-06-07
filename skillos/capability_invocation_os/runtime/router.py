"""Deny-by-default router — disabled returns DENY_NOOP."""
from skillos.capability_invocation_os.runtime.models import InvocationRequest, InvocationDecision, RouterResult
from skillos.capability_invocation_os.runtime.config import is_runtime_enabled

def classify_request(request): return {"intent": "unknown", "tier": "T5", "action": "DENY"}
def select_candidate_capabilities(request, registry=None): return []
def route(request, registry=None, config=None):
    if config and not is_runtime_enabled(config): return InvocationDecision(action="DENY_NOOP", reason="runtime disabled", evidence_required=True)
    return InvocationDecision(action="DENY", reason="router disabled by default", evidence_required=True)
