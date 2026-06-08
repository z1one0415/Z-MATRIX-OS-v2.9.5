import pytest
from skillos.capability_invocation_os.adapters.wave0.controlled_readonly import ControlledReadonlyDecision
from skillos.capability_invocation_os.adapters.wave0.canary import CanaryPlan, CanaryPhase
def test_decision_no_envelope_fields():
    d = ControlledReadonlyDecision()
    assert not hasattr(d, 'result_envelope')
    assert not hasattr(d, 'caller_visible_message')
    assert not hasattr(d, 'execute')
def test_canary_plan_no_envelope():
    p = CanaryPlan(phase=CanaryPhase.PHASE_1_SYNTHETIC)
    assert not hasattr(p, 'result_envelope')
