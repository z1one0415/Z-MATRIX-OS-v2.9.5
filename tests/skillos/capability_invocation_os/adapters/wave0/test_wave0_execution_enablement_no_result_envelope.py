"""Proof: no result_envelope mutation — enablement layer does not touch envelopes."""
import pytest
from skillos.capability_invocation_os.adapters.wave0.decision import (
    Wave0EnablementDecision, Wave0EnablementReason,
    Wave0EnablementBoundary, Wave0EnablementProofHint,
)
from skillos.capability_invocation_os.adapters.wave0.enablement import (
    plan_wave0_enablement, EnablementDecision,
)
from skillos.capability_invocation_os.adapters.wave0.config import Wave0ExecutionConfig
from skillos.capability_invocation_os.adapters.wave0.models import Wave0AdapterKind


def test_enablement_decision_no_envelope_fields():
    """EnablementDecision has no result_envelope mutation fields."""
    d = Wave0EnablementDecision()
    assert not hasattr(d, 'result_envelope')
    assert not hasattr(d, 'mutate_envelope')
    assert not hasattr(d, 'caller_message')


def test_boundary_all_true():
    """All boundary guards must be True."""
    b = Wave0EnablementBoundary()
    assert b.no_runtime_enablement is True
    assert b.no_adapter_execution is True
    assert b.no_capability_execution is True
    assert b.no_real_adapter_call is True
    assert b.no_network_call is True
    assert b.no_file_read_write is True
    assert b.no_zmatrix_import is True
    assert b.no_warning_enablement is True
    assert b.no_result_envelope_mutation is True
    assert b.no_blocking is True
    assert b.no_fail_closed is True
    assert b.no_production is True
    assert b.level5_blocked is True


def test_decision_default_denied():
    d = Wave0EnablementDecision()
    assert d.allowed is False
    assert d.reason == Wave0EnablementReason.DISABLED_DEFAULT


def test_proof_hints_valid():
    hints = Wave0EnablementProofHint()
    assert len(hints.disabled_default_proofs) >= 4
    assert len(hints.triple_gate_proofs) >= 2
    assert len(hints.kill_switch_proofs) >= 3
    assert len(hints.permission_proofs) >= 4


def test_enablement_result_no_caller_fields():
    cfg = Wave0ExecutionConfig()
    result = plan_wave0_enablement(cfg, Wave0AdapterKind.GITHUB_READONLY)
    assert not hasattr(result, 'caller_visible_message')
    assert not hasattr(result, 'result_envelope')
    assert not hasattr(result, 'execute')
    assert not hasattr(result, 'run')
    assert not hasattr(result, 'call')
    assert not hasattr(result, 'invoke')
