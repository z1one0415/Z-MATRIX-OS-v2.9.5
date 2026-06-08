"""Proof: no side effects — no file writes, no stdout, no runtime artifacts."""
import os
import sys
import pytest
from skillos.capability_invocation_os.adapters.wave0.config import Wave0ExecutionConfig
from skillos.capability_invocation_os.adapters.wave0.enablement import (
    plan_wave0_enablement, request_wave0_enablement, deny_wave0_execution,
    describe_enablement_state,
)
from skillos.capability_invocation_os.adapters.wave0.failsafe import (
    degrade_enablement_to_noop, degrade_enablement_to_plan_only,
    deny_enablement_without_exception,
)
from skillos.capability_invocation_os.adapters.wave0.models import Wave0AdapterKind


def test_enablement_functions_no_file_write(tmp_path):
    """Enablement functions don't write files."""
    pre_files = set(os.listdir(tmp_path))
    cfg = Wave0ExecutionConfig()
    plan_wave0_enablement(cfg, Wave0AdapterKind.GITHUB_READONLY)
    request_wave0_enablement(cfg, Wave0AdapterKind.GITHUB_READONLY)
    deny_wave0_execution("test")
    describe_enablement_state(cfg)
    post_files = set(os.listdir(tmp_path))
    assert pre_files == post_files


def test_failsafe_no_file_write(tmp_path):
    """Failsafe functions don't write files."""
    pre_files = set(os.listdir(tmp_path))
    degrade_enablement_to_noop()
    degrade_enablement_to_plan_only()
    deny_enablement_without_exception()
    post_files = set(os.listdir(tmp_path))
    assert pre_files == post_files


def test_no_runtime_audit_created():
    """No runtime_audit directory created."""
    assert not os.path.exists("runtime_audit")
    assert not os.path.exists("runtime_reports")


def test_decisions_are_internal_only():
    """Enablement decisions don't produce caller-visible output."""
    cfg = Wave0ExecutionConfig()
    result = plan_wave0_enablement(cfg, Wave0AdapterKind.GITHUB_READONLY)
    assert not hasattr(result, 'caller_visible')
    assert not hasattr(result, 'stdout_message')
