import pytest
from skillos.capability_invocation_os.adapters.wave0.canary import (
    plan_synthetic_canary, plan_provided_input_canary,
    reject_external_source_canary, evaluate_canary_boundary,
    CanaryPhase,
)
from skillos.capability_invocation_os.adapters.wave0.models import Wave0AdapterKind
from skillos.capability_invocation_os.adapters.wave0.controlled_readonly import ControlledInputKind, ControlledReadonlyMode

def test_synthetic_canary_plan_only():
    plan = plan_synthetic_canary(Wave0AdapterKind.REPORT_READING)
    assert plan.phase == CanaryPhase.PHASE_1_SYNTHETIC
    assert plan.allowed is False

def test_provided_canary_plan_only():
    plan = plan_provided_input_canary(Wave0AdapterKind.DOCUMENT_GENERATION)
    assert plan.allowed is False

def test_external_source_rejected():
    plan = reject_external_source_canary()
    assert plan.allowed is False

def test_canary_boundary_denies_external():
    result = evaluate_canary_boundary(ControlledInputKind.EXTERNAL)
    assert result.mode == ControlledReadonlyMode.DENY_NOOP

def test_canary_boundary_denies_github():
    result = evaluate_canary_boundary(ControlledInputKind.GITHUB_METADATA)
    assert result.mode == ControlledReadonlyMode.DENY_NOOP
