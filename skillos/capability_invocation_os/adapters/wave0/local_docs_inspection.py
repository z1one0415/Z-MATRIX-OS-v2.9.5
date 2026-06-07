"""Local docs inspection adapter skeleton — no file read, no mutation, no execution."""
from skillos.capability_invocation_os.adapters.wave0.models import Wave0Decision, LocalDocsInspectionPlan
class LocalDocsInspectionAdapterSkeleton:
    def __init__(self): self._plan = LocalDocsInspectionPlan()
    def supported_future_actions(self): return self._plan.future_actions
    def validate_docs_request(self): return Wave0Decision(action="DENY",reason="docs inspection disabled")
    def deny(self): return Wave0Decision(action="DENY",reason="docs inspection denied")
