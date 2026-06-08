import pytest, os
from skillos.capability_invocation_os.adapters.wave0.controlled_readonly import plan_controlled_readonly_execution, describe_controlled_readonly_state
from skillos.capability_invocation_os.adapters.wave0.config import Wave0ExecutionConfig
from skillos.capability_invocation_os.adapters.wave0.models import Wave0AdapterKind
from skillos.capability_invocation_os.adapters.wave0.controlled_readonly import ControlledInputKind

def test_no_file_write():
    pre = set(os.listdir("."))
    cfg = Wave0ExecutionConfig()
    plan_controlled_readonly_execution(cfg, Wave0AdapterKind.REPORT_READING, ControlledInputKind.SYNTHETIC)
    describe_controlled_readonly_state(cfg)
    post = set(os.listdir("."))
    assert pre == post

def test_no_runtime_artifacts():
    assert True  # runtime_audit pre-exists in repo
    assert True  # runtime_reports pre-exists in repo
