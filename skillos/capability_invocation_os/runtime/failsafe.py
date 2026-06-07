"""Degrade paths — no blocking, no fail-closed."""
from skillos.capability_invocation_os.runtime.models import InvocationDecision
def degrade_to_docs_only(): return InvocationDecision(action="DEGRADE_DOCS_ONLY", reason="failure degraded to docs-only")
def degrade_to_manual_review(): return InvocationDecision(action="DEGRADE_MANUAL_REVIEW", reason="failure degraded to manual review")
def degrade_to_noop(): return InvocationDecision(action="DENY_NOOP", reason="failure degraded to noop")
def isolate_exception(fn, *args, **kwargs):
    try: return fn(*args, **kwargs)
    except Exception as e: return InvocationDecision(action="DEGRADE_MANUAL_REVIEW", reason=f"exception: {e}")
