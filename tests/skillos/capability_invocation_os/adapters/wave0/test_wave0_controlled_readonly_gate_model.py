import pytest
from skillos.capability_invocation_os.adapters.wave0.gates import (
    evaluate_controlled_readonly_gate, ControlledReadonlyGateDecision,
)
from skillos.capability_invocation_os.adapters.wave0.config import Wave0ExecutionConfig
from skillos.capability_invocation_os.adapters.wave0.models import Wave0AdapterKind
from skillos.capability_invocation_os.adapters.wave0.controlled_readonly import ControlledInputKind

def test_seven_gate_default_deny():
    result = evaluate_controlled_readonly_gate(Wave0ExecutionConfig(), Wave0AdapterKind.REPORT_READING, ControlledInputKind.SYNTHETIC)
    assert result.final == "DENY_DISABLED"
    assert "P0" in result.reason

def test_all_gates_disabled():
    result = evaluate_controlled_readonly_gate(Wave0ExecutionConfig(), Wave0AdapterKind.DOCUMENT_GENERATION, ControlledInputKind.PROVIDED)
    assert result.final == "DENY_DISABLED"
