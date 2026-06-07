"""Composition guard — multi-skill chains denied by default."""
from skillos.capability_invocation_os.runtime.models import InvocationRequest, InvocationDecision, RiskTier
def validate_chain(requests):
    if not requests: return InvocationDecision(action="DENY", reason="empty chain")
    if len(requests) > 1: return InvocationDecision(action="DENY", reason="multi-skill chain disabled by default")
    return InvocationDecision(action="DENY_NOOP", reason="composition disabled by default")
def detect_forbidden_composition(requests):
    tiers = [getattr(getattr(r, "capability_id", None), "risk_tier", RiskTier.T5) for r in requests]
    return RiskTier.T5 in tiers
def detect_conflict(requests): return len(set(r.caller_role for r in requests)) > 1
def plan_evidence_handoff(requests): return len(requests)
