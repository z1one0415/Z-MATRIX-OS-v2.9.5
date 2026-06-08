import pytest
from skillos.capability_invocation_os.adapters.wave0.controlled_readonly import plan_controlled_readonly_execution, describe_controlled_readonly_state, ControlledInputKind
from skillos.capability_invocation_os.adapters.wave0.config import Wave0ExecutionConfig; from skillos.capability_invocation_os.adapters.wave0.models import Wave0AdapterKind
def test_never_raises():
    try:
        for k in Wave0AdapterKind:
            for i in ControlledInputKind:
                plan_controlled_readonly_execution(Wave0ExecutionConfig(),k,i)
        describe_controlled_readonly_state(Wave0ExecutionConfig())
    except: pytest.fail("Raised")
def test_no_block():
    r=plan_controlled_readonly_execution(Wave0ExecutionConfig(),Wave0AdapterKind.REPORT_READING,ControlledInputKind.SYNTHETIC)
    assert "BLOCK" not in str(r.mode)
