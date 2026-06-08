import pytest
from skillos.capability_invocation_os.adapters.wave0.controlled_readonly import (
    plan_controlled_readonly_execution, ControlledInputKind,
)
from skillos.capability_invocation_os.adapters.wave0.config import Wave0ExecutionConfig
from skillos.capability_invocation_os.adapters.wave0.models import Wave0AdapterKind

def test_plan_does_not_execute():
    cfg = Wave0ExecutionConfig()
    result = plan_controlled_readonly_execution(cfg, Wave0AdapterKind.REPORT_READING, ControlledInputKind.SYNTHETIC)
    assert result.mode.value != "EXECUTE"
    assert "EXECUTE" not in str(result.mode)

def test_github_metadata_does_not_call():
    cfg = Wave0ExecutionConfig()
    result = plan_controlled_readonly_execution(cfg, Wave0AdapterKind.GITHUB_READONLY, ControlledInputKind.GITHUB_METADATA)
    assert "DENY" in result.mode.value
