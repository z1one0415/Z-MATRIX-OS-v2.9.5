import pytest, os
from skillos.capability_invocation_os.adapters.wave0.controlled_readonly import plan_controlled_readonly_execution, describe_controlled_readonly_state
from skillos.capability_invocation_os.adapters.wave0.config import Wave0ExecutionConfig; from skillos.capability_invocation_os.adapters.wave0.models import Wave0AdapterKind; from skillos.capability_invocation_os.adapters.wave0.controlled_readonly import ControlledInputKind
def test_no_file_write():
    pre=set(os.listdir("."))
    plan_controlled_readonly_execution(Wave0ExecutionConfig(),Wave0AdapterKind.REPORT_READING,ControlledInputKind.SYNTHETIC)
    describe_controlled_readonly_state(Wave0ExecutionConfig())
    assert pre==set(os.listdir("."))
