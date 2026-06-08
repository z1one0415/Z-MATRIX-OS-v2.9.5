"""Wave0 Failsafe — no blocking, no fail-closed, no exception to caller.

- degrade_enablement_to_noop
- degrade_enablement_to_plan_only
- deny_enablement_without_exception
- no blocking
- no fail-closed
- no caller exception
"""

from dataclasses import dataclass, field
from typing import Optional
from skillos.capability_invocation_os.adapters.wave0.models import Wave0Decision


@dataclass(frozen=True)
class FailsafeDecision:
    action: str
    reason: str
    escalated: bool = False
    requires_manual_review: bool = False


def degrade_to_noop() -> FailsafeDecision:
    """Degrade any action to NOOP. No exception raised."""
    return FailsafeDecision(action="DENY_NOOP", reason="degraded to noop")


def degrade_to_plan_only() -> FailsafeDecision:
    """Degrade to plan-only mode. No execution."""
    return FailsafeDecision(action="PLAN_ONLY", reason="degraded to plan only")


def degrade_to_manual_review() -> FailsafeDecision:
    """Escalate to manual review. No automatic action."""
    return FailsafeDecision(
        action="MANUAL_REVIEW",
        reason="escalated to manual review",
        escalated=True,
        requires_manual_review=True,
    )


def deny_wave0_adapter() -> FailsafeDecision:
    """Deny adapter execution. No exception."""
    return FailsafeDecision(action="DENY", reason="wave0 adapter execution denied")


def deny_enablement_without_exception(reason: str = "enablement denied") -> FailsafeDecision:
    """Deny enablement. No exception raised. No blocking. No fail-closed."""
    return FailsafeDecision(action="DENY", reason=reason)


def degrade_enablement_to_noop(
    original_action: Optional[str] = None,
) -> FailsafeDecision:
    """Degrade enablement to NOOP. Safe default for any unexpected state."""
    detail = f"degraded from {original_action}" if original_action else "degraded"
    return FailsafeDecision(action="DENY_NOOP", reason=detail)


def degrade_enablement_to_plan_only(
    original_action: Optional[str] = None,
) -> FailsafeDecision:
    """Degrade enablement to PLAN_ONLY. No execution, planning still possible."""
    detail = f"degraded from {original_action} to plan only" if original_action else "degraded to plan only"
    return FailsafeDecision(action="PLAN_ONLY", reason=detail)


# Backward-compatible aliases
def _degrade_to_noop():
    return Wave0Decision(action="DENY_NOOP", reason="degraded")


def _degrade_to_plan_only():
    return Wave0Decision(action="PLAN_ONLY", reason="degraded to plan")


def _degrade_to_manual_review():
    return Wave0Decision(action="MANUAL_REVIEW", reason="escalated")


def _deny_wave0_adapter():
    return Wave0Decision(action="DENY", reason="wave0 adapter denied")


def degrade_controlled_readonly_to_noop():
    from .failsafe import FailsafeDecision
    return FailsafeDecision(action="DENY_NOOP", reason="degraded to noop")
def degrade_controlled_readonly_to_plan_only():
    from .failsafe import FailsafeDecision
    return FailsafeDecision(action="PLAN_ONLY", reason="degraded to plan only")
def deny_controlled_readonly_without_exception(reason: str = "denied"):
    from .failsafe import FailsafeDecision
    return FailsafeDecision(action="DENY", reason=reason)
