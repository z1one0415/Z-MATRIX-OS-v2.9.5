import pytest
from skillos.capability_invocation_os.adapters.wave0.canary import plan_synthetic_canary, plan_provided_input_canary, reject_external_source_canary, evaluate_canary_boundary, CanaryPhase
from skillos.capability_invocation_os.adapters.wave0.models import Wave0AdapterKind
from skillos.capability_invocation_os.adapters.wave0.controlled_readonly import ControlledInputKind, ControlledReadonlyMode
def test_synthetic_plan_only():
    p = plan_synthetic_canary(Wave0AdapterKind.REPORT_READING)
    assert p.allowed is False
def test_external_rejected():
    p = reject_external_source_canary()
    assert p.allowed is False
def test_boundary_denies_external():
    r = evaluate_canary_boundary(ControlledInputKind.EXTERNAL)
    assert r.mode == ControlledReadonlyMode.DENY_NOOP
def test_boundary_denies_github():
    r = evaluate_canary_boundary(ControlledInputKind.GITHUB_METADATA)
    assert r.mode == ControlledReadonlyMode.DENY_NOOP
