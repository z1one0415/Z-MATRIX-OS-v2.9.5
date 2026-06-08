import pytest
from skillos.capability_invocation_os.adapters.wave0.controlled_readonly import (
    plan_controlled_readonly_execution, deny_controlled_readonly_execution,
    describe_controlled_readonly_state, ControlledInputKind,
)
from skillos.capability_invocation_os.adapters.wave0.config import Wave0ExecutionConfig
from skillos.capability_invocation_os.adapters.wave0.models import Wave0AdapterKind

def test_controlled_functions_never_raise():
    cfg = Wave0ExecutionConfig()
    try:
        for kind in Wave0AdapterKind:
            for input_kind in ControlledInputKind:
                plan_controlled_readonly_execution(cfg, kind, input_kind)
        deny_controlled_readonly_execution("test")
        describe_controlled_readonly_state(cfg)
    except Exception as e:
        pytest.fail(f"Controlled function raised: {e}")

def test_no_blocking_actions():
    result = plan_controlled_readonly_execution(Wave0ExecutionConfig(), Wave0AdapterKind.REPORT_READING, ControlledInputKind.SYNTHETIC)
    assert "BLOCK" not in result.mode.value
