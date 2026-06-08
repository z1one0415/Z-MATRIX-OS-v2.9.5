"""Proof: default disabled — all enabled functions return False."""
import pytest
from skillos.capability_invocation_os.adapters.wave0.config import (
    Wave0ExecutionConfig, is_wave0_runtime_enabled,
    is_wave0_adapter_framework_enabled, is_github_readonly_execution_enabled,
    is_document_generation_execution_enabled, is_local_docs_inspection_execution_enabled,
    is_report_reading_execution_enabled, env_override,
)


def test_default_config_all_disabled():
    cfg = Wave0ExecutionConfig()
    assert is_wave0_runtime_enabled(cfg) is False
    assert is_wave0_adapter_framework_enabled(cfg) is False
    assert is_github_readonly_execution_enabled(cfg) is False
    assert is_document_generation_execution_enabled(cfg) is False
    assert is_local_docs_inspection_execution_enabled(cfg) is False
    assert is_report_reading_execution_enabled(cfg) is False


def test_env_cannot_enable():
    assert env_override() is False


def test_requested_true_does_not_enable():
    cfg = Wave0ExecutionConfig(wave0_runtime_requested=True)
    assert cfg.wave0_runtime_requested is True
    assert is_wave0_runtime_enabled(cfg) is False  # requested != enabled


def test_all_requested_true_still_disabled():
    cfg = Wave0ExecutionConfig(
        wave0_runtime_requested=True,
        wave0_adapter_framework_requested=True,
        wave0_github_readonly_requested=True,
        wave0_document_generation_requested=True,
        wave0_local_docs_inspection_requested=True,
        wave0_report_reading_requested=True,
    )
    assert is_wave0_runtime_enabled(cfg) is False
    assert is_github_readonly_execution_enabled(cfg) is False
    assert is_document_generation_execution_enabled(cfg) is False


def test_from_dict_none():
    cfg = Wave0ExecutionConfig.from_dict(None)
    assert cfg.wave0_runtime_requested is False
