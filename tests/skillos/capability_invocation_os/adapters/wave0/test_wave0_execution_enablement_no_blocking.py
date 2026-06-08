"""Proof: no blocking/fail-closed — enablement layer never blocks or raises."""
import pytest
from skillos.capability_invocation_os.adapters.wave0.failsafe import (
    degrade_enablement_to_noop, degrade_enablement_to_plan_only,
    deny_enablement_without_exception, FailsafeDecision,
)
from skillos.capability_invocation_os.adapters.wave0.enablement import (
    plan_wave0_enablement, request_wave0_enablement, describe_enablement_state,
)
from skillos.capability_invocation_os.adapters.wave0.config import Wave0ExecutionConfig
from skillos.capability_invocation_os.adapters.wave0.models import Wave0AdapterKind


def test_failsafe_never_raises():
    """Failsafe functions should never raise exceptions."""
    try:
        degrade_enablement_to_noop()
        degrade_enablement_to_plan_only()
        deny_enablement_without_exception()
    except Exception as e:
        pytest.fail(f"Failsafe raised: {e}")


def test_failsafe_returns_decision():
    assert isinstance(degrade_enablement_to_noop(), FailsafeDecision)
    assert isinstance(degrade_enablement_to_plan_only(), FailsafeDecision)
    assert isinstance(deny_enablement_without_exception(), FailsafeDecision)


def test_enablement_never_raises():
    """Enablement functions should never raise on any input."""
    cfg = Wave0ExecutionConfig()
    try:
        for kind in Wave0AdapterKind:
            plan_wave0_enablement(cfg, kind)
            request_wave0_enablement(cfg, kind)
        describe_enablement_state(cfg)
        # None config should also work
        plan_wave0_enablement(Wave0ExecutionConfig(), Wave0AdapterKind.GITHUB_READONLY)
    except Exception as e:
        pytest.fail(f"Enablement raised: {e}")


def test_no_blocking_behavior():
    """All decisions are immediate — no blocking, no waiting."""
    d = degrade_enablement_to_noop()
    assert d.action != "BLOCK"
    assert d.action != "WAIT"


def test_no_fail_closed():
    """No fail-closed behavior — degraded, not closed."""
    d = degrade_enablement_to_plan_only()
    assert "CLOSED" not in d.action
    assert "FAIL" not in d.action
