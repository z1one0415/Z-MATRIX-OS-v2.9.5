import pytest
from skillos.capability_invocation_os.adapters.wave0.config import is_controlled_readonly_enabled, is_controlled_report_reading_enabled, is_controlled_document_generation_enabled, is_controlled_github_metadata_enabled, Wave0ExecutionConfig
from skillos.capability_invocation_os.adapters.wave0.controlled_readonly import plan_controlled_readonly_execution, ControlledReadonlyMode, ControlledInputKind, describe_controlled_readonly_state
from skillos.capability_invocation_os.adapters.wave0.models import Wave0AdapterKind

def test_all_enabled_false():
    cfg = Wave0ExecutionConfig()
    assert is_controlled_readonly_enabled(cfg) is False
    assert is_controlled_report_reading_enabled(cfg) is False
    assert is_controlled_document_generation_enabled(cfg) is False
    assert is_controlled_github_metadata_enabled(cfg) is False

def test_plan_always_canary():
    cfg = Wave0ExecutionConfig()
    r = plan_controlled_readonly_execution(cfg, Wave0AdapterKind.REPORT_READING, ControlledInputKind.SYNTHETIC)
    assert r.mode == ControlledReadonlyMode.CANARY_PLAN_ONLY

def test_external_source_denied():
    r = plan_controlled_readonly_execution(Wave0ExecutionConfig(), Wave0AdapterKind.GITHUB_READONLY, ControlledInputKind.EXTERNAL)
    assert r.mode == ControlledReadonlyMode.DENY_NOOP

def test_github_metadata_denied():
    r = plan_controlled_readonly_execution(Wave0ExecutionConfig(), Wave0AdapterKind.GITHUB_READONLY, ControlledInputKind.GITHUB_METADATA)
    assert r.mode == ControlledReadonlyMode.DENY_NOOP

def test_describe_state():
    s = describe_controlled_readonly_state(Wave0ExecutionConfig())
    assert "DISABLED" in s["controlled_readonly"]
