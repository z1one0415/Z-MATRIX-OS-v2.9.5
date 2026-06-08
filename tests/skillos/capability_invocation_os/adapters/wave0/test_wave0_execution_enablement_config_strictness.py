"""Proof: config strictness — non-bool, env, malformed, missing → disabled."""
import pytest
from skillos.capability_invocation_os.adapters.wave0.config import Wave0ExecutionConfig


def test_non_bool_truthy_disabled():
    """Non-bool truthy values (string 'true', 1) are treated as not-requested."""
    cfg = Wave0ExecutionConfig.from_dict({
        "WAVE0_RUNTIME_ENABLED": "true",
        "WAVE0_GITHUB_READONLY_ENABLED": 1,
        "WAVE0_DOCUMENT_GENERATION_ENABLED": "True",
    })
    assert cfg.wave0_runtime_requested is False
    assert cfg.wave0_github_readonly_requested is False


def test_malformed_config_disabled():
    """Malformed config keys don't enable anything."""
    cfg = Wave0ExecutionConfig.from_dict({"UNKNOWN_KEY": True})
    assert cfg.wave0_runtime_requested is False


def test_missing_config_disabled():
    """Missing config → all disabled."""
    cfg = Wave0ExecutionConfig.from_dict({})
    assert not any([
        cfg.wave0_runtime_requested, cfg.wave0_adapter_framework_requested,
        cfg.wave0_github_readonly_requested, cfg.wave0_document_generation_requested,
        cfg.wave0_local_docs_inspection_requested, cfg.wave0_report_reading_requested,
    ])


def test_only_explicit_true_accepted():
    """Only True (the bool, not string, not 1) is accepted as requested."""
    cfg = Wave0ExecutionConfig.from_dict({
        "WAVE0_GITHUB_READONLY_ENABLED": True,
        "WAVE0_DOCUMENT_GENERATION_ENABLED": False,
    })
    assert cfg.wave0_github_readonly_requested is True  # strict True accepted
    assert cfg.wave0_document_generation_requested is False  # explicit False


def test_not_dict_input():
    cfg = Wave0ExecutionConfig.from_dict("not a dict")
    assert cfg.wave0_runtime_requested is False
