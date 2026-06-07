"""GitHub read-only adapter skeleton — no API calls, no network, no write."""
from skillos.capability_invocation_os.adapters.wave0.models import Wave0Decision, GitHubReadOnlyPlan
class GitHubReadOnlyAdapterSkeleton:
    def __init__(self): self._plan = GitHubReadOnlyPlan()
    def supported_future_actions(self): return self._plan.future_actions
    def forbidden_actions(self): return self._plan.forbidden_actions
    def validate_readonly_request(self): return Wave0Decision(action="DENY",reason="GitHub adapter disabled")
    def plan_evidence(self): return Wave0Decision(action="DENY",reason="evidence disabled")
    def deny(self): return Wave0Decision(action="DENY",reason="GitHub adapter denied")
