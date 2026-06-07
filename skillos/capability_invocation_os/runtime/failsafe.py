"""Degrade paths — no fail-closed, no blocking."""
from skillos.capability_invocation_os.runtime.models import InvocationDecision

def degrade_to_docs_only() -> InvocationDecision:
    return InvocationDecision(action="DEGRADE_DOCS_ONLY", reason="failure degraded to docs-only")

def degrade_to_manual_review() -> InvocationDecision:
    return InvocationDecision(action="DEGRADE_MANUAL_REVIEW", reason="failure degraded to manual review")
