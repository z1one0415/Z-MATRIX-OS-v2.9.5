import pytest
from skillos.capability_invocation_os.adapters.wave0.controlled_readonly import plan_controlled_readonly_execution, ControlledInputKind
from skillos.capability_invocation_os.adapters.wave0.config import Wave0ExecutionConfig; from skillos.capability_invocation_os.adapters.wave0.models import Wave0AdapterKind
def test_does_not_execute():
    r=plan_controlled_readonly_execution(Wave0ExecutionConfig(),Wave0AdapterKind.REPORT_READING,ControlledInputKind.SYNTHETIC)
    assert "EXECUTE" not in str(r.mode)
def test_github_does_not_call():
    r=plan_controlled_readonly_execution(Wave0ExecutionConfig(),Wave0AdapterKind.GITHUB_READONLY,ControlledInputKind.GITHUB_METADATA)
    assert "DENY" in str(r.mode)
