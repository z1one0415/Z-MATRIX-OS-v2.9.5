"""Wave0 failsafe — no blocking, no fail-closed, no exception to caller."""
from skillos.capability_invocation_os.adapters.wave0.models import Wave0Decision
def degrade_to_noop(): return Wave0Decision(action="DENY_NOOP",reason="degraded")
def degrade_to_plan_only(): return Wave0Decision(action="PLAN_ONLY",reason="degraded to plan")
def degrade_to_manual_review(): return Wave0Decision(action="MANUAL_REVIEW",reason="escalated")
def deny_wave0_adapter(): return Wave0Decision(action="DENY",reason="wave0 adapter denied")
