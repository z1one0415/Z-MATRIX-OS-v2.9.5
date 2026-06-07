"""Wave0 adapter skeleton — no execute/run/call/invoke, no network, no file I/O."""
from skillos.capability_invocation_os.adapters.wave0.models import Wave0Request, Wave0Decision
class Wave0AdapterSkeleton:
    def describe(self): return {"status":"disabled","wave":"0","kind":"readonly"}
    def validate_request(self,r): return Wave0Decision(action="DENY",reason="validation disabled")
    def plan_evidence(self): return Wave0Decision(action="DENY",reason="evidence planning disabled")
    def deny(self): return Wave0Decision(action="DENY",reason="adapter denied by default")
    def degrade(self): return Wave0Decision(action="DENY_NOOP",reason="degraded to noop")
