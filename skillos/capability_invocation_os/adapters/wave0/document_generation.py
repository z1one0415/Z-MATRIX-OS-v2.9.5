"""Document generation adapter skeleton — no file write, no publish, no execution."""
from skillos.capability_invocation_os.adapters.wave0.models import Wave0Decision, DocumentGenerationPlan
class DocumentGenerationAdapterSkeleton:
    def __init__(self): self._plan = DocumentGenerationPlan()
    def supported_future_outputs(self): return self._plan.future_outputs
    def validate_generation_request(self): return Wave0Decision(action="DENY",reason="generation disabled")
    def plan_output_hash(self): return Wave0Decision(action="DENY",reason="hash planning disabled")
    def deny(self): return Wave0Decision(action="DENY",reason="doc generation denied")
