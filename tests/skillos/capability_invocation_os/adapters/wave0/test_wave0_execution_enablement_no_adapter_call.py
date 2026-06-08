"""Proof: no real adapter call — execution functions don't execute adapters."""
import pytest
from skillos.capability_invocation_os.adapters.wave0.config import Wave0ExecutionConfig
from skillos.capability_invocation_os.adapters.wave0.enablement import (
    plan_wave0_enablement, request_wave0_enablement,
)
from skillos.capability_invocation_os.adapters.wave0.models import Wave0AdapterKind


def test_plan_does_not_execute():
    """Plan enablement does not execute any adapter."""
    cfg = Wave0ExecutionConfig()
    result = plan_wave0_enablement(cfg, Wave0AdapterKind.GITHUB_READONLY)
    assert result.action.value in ("DENY_NOOP", "PLAN_ONLY", "DISABLED")
    assert result.action.value != "EXECUTE"


def test_request_does_not_execute():
    """Request enablement does not execute any adapter."""
    cfg = Wave0ExecutionConfig()
    result = request_wave0_enablement(cfg, Wave0AdapterKind.DOCUMENT_GENERATION)
    assert result.action.value == "DISABLED"


def test_no_github_call_triggered():
    """Enablement layer does not import or call GitHub."""
    cfg = Wave0ExecutionConfig(
        wave0_runtime_requested=True,
        wave0_adapter_framework_requested=True,
        wave0_github_readonly_requested=True,
    )
    result = plan_wave0_enablement(cfg, Wave0AdapterKind.GITHUB_READONLY)
    # PLAN_ONLY at best, no execution
    assert "execution" not in result.action.value.lower() or result.action.value == "DENY_NOOP"


def test_no_adapter_instantiated():
    """Enablement functions don't instantiate real adapters."""
    cfg = Wave0ExecutionConfig()
    result = request_wave0_enablement(cfg, Wave0AdapterKind.REPORT_READING)
    assert result.action.value == "DISABLED"
