"""AdapterBase — skeleton only, no execute/run/call/invoke methods, no Z-MATRIX imports."""
from skillos.capability_invocation_os.adapters.models import AdapterDescriptor, AdapterRequest, AdapterDecision
class AdapterBase:
    def __init__(self): self._descriptor = AdapterDescriptor()
    def describe(self): return self._descriptor
    def validate_contract(self): return AdapterDecision(action="DENY", reason="contract validation disabled")
    def plan_evidence(self): return AdapterDecision(action="DENY", reason="evidence planning disabled")
    def degrade(self): return AdapterDecision(action="DENY_NOOP", reason="degraded to noop")
    def deny(self): return AdapterDecision(action="DENY", reason="adapter denied by default")
