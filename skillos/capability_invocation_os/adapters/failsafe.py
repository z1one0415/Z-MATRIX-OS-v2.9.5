"""Adapter failsafe — no blocking, no fail-closed, no Z-MATRIX imports."""
from skillos.capability_invocation_os.adapters.models import AdapterDecision
def degrade_to_no_adapter(): return AdapterDecision(action="DENY_NOOP", reason="no adapter available")
def degrade_to_docs_only(): return AdapterDecision(action="DEGRADE_DOCS_ONLY", reason="degraded to docs-only")
def degrade_to_manual_review(): return AdapterDecision(action="DEGRADE_MANUAL_REVIEW", reason="escalated to manual review")
def deny_adapter_execution(): return AdapterDecision(action="DENY", reason="adapter execution denied")
