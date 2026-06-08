import pytest
from skillos.capability_invocation_os.adapters.wave0.config import (
    is_controlled_readonly_enabled, is_controlled_report_reading_enabled,
    is_controlled_document_generation_enabled, is_controlled_local_docs_inspection_enabled,
    is_controlled_github_metadata_enabled,
)
from skillos.capability_invocation_os.adapters.wave0.controlled_readonly import (
    plan_controlled_readonly_execution, ControlledReadonlyMode,
    ControlledInputKind, describe_controlled_readonly_state,
)
from skillos.capability_invocation_os.adapters.wave0.config import Wave0ExecutionConfig
from skillos.capability_invocation_os.adapters.wave0.models import Wave0AdapterKind

def test_all_controlled_enabled_false():
    cfg = Wave0ExecutionConfig()
    assert is_controlled_readonly_enabled(cfg) is False
    assert is_controlled_report_reading_enabled(cfg) is False
    assert is_controlled_document_generation_enabled(cfg) is False

def test_plan_always_disabled_or_canary():
    cfg = Wave0ExecutionConfig()
    result = plan_controlled_readonly_execution(cfg, Wave0AdapterKind.REPORT_READING, ControlledInputKind.SYNTHETIC)
    assert result.mode in (ControlledReadonlyMode.DISABLED, ControlledReadonlyMode.CANARY_PLAN_ONLY)

def test_external_source_denied():
    cfg = Wave0ExecutionConfig()
    result = plan_controlled_readonly_execution(cfg, Wave0AdapterKind.GITHUB_READONLY, ControlledInputKind.EXTERNAL)
    assert result.mode == ControlledReadonlyMode.DENY_NOOP

def test_github_metadata_denied():
    cfg = Wave0ExecutionConfig()
    result = plan_controlled_readonly_execution(cfg, Wave0AdapterKind.GITHUB_READONLY, ControlledInputKind.GITHUB_METADATA)
    assert result.mode == ControlledReadonlyMode.DENY_NOOP

def test_describe_returns_disabled():
    state = describe_controlled_readonly_state(Wave0ExecutionConfig())
    assert "DISABLED" in state["controlled_readonly"] or "DENIED" in state["github_metadata"]
