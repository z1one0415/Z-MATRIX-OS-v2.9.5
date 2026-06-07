"""Report reading adapter skeleton — no report write, no execution."""
from skillos.capability_invocation_os.adapters.wave0.models import Wave0Decision, ReportReadingPlan
class ReportReadingAdapterSkeleton:
    def __init__(self): self._plan = ReportReadingPlan()
    def supported_future_actions(self): return self._plan.future_actions
    def validate_report_request(self): return Wave0Decision(action="DENY",reason="report reading disabled")
    def deny(self): return Wave0Decision(action="DENY",reason="report reading denied")
