"""Proof: triple gate — gate evaluation always returns DENY/PLAN_ONLY in P0."""
import pytest
from skillos.capability_invocation_os.adapters.wave0.config import Wave0ExecutionConfig
from skillos.capability_invocation_os.adapters.wave0.gates import (
    Wave0GateDecision, Wave0GateState, evaluate_wave0_triple_gate, Wave0TripleGateDecision,
)
from skillos.capability_invocation_os.adapters.wave0.models import Wave0AdapterKind


def test_triple_gate_default_all_disabled():
    cfg = Wave0ExecutionConfig()
    result = evaluate_wave0_triple_gate(cfg, Wave0AdapterKind.GITHUB_READONLY)
    assert result.final == Wave0GateDecision.DENY_DISABLED
    assert result.runtime_gate == Wave0GateState.DISABLED


def test_all_requested_still_plan_only():
    cfg = Wave0ExecutionConfig(
        wave0_runtime_requested=True,
        wave0_adapter_framework_requested=True,
        wave0_github_readonly_requested=True,
    )
    result = evaluate_wave0_triple_gate(cfg, Wave0AdapterKind.GITHUB_READONLY)
    # P0: all requested → PLAN_ONLY, not ENABLED
    assert result.final == Wave0GateDecision.PLAN_ONLY
    assert "execution not enabled" in result.reason


def test_any_gate_missing_denied():
    cfg = Wave0ExecutionConfig(
        wave0_runtime_requested=True,
        wave0_adapter_framework_requested=True,
    )
    result = evaluate_wave0_triple_gate(cfg, Wave0AdapterKind.GITHUB_READONLY)
    assert result.final == Wave0GateDecision.DENY_DISABLED


def test_all_adapters_gate():
    for kind in Wave0AdapterKind:
        cfg = Wave0ExecutionConfig()
        result = evaluate_wave0_triple_gate(cfg, kind)
        assert result.final == Wave0GateDecision.DENY_DISABLED


def test_no_enabled_state_exists():
    """Verify that no gate state equals 'ENABLED' in P0."""
    assert not hasattr(Wave0GateState, 'ENABLED')
