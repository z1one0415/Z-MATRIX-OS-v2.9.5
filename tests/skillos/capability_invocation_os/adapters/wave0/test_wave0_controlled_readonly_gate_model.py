import pytest
from skillos.capability_invocation_os.adapters.wave0.gates import evaluate_controlled_readonly_gate, ControlledReadonlyGateDecision
from skillos.capability_invocation_os.adapters.wave0.config import Wave0ExecutionConfig
from skillos.capability_invocation_os.adapters.wave0.models import Wave0AdapterKind
from skillos.capability_invocation_os.adapters.wave0.controlled_readonly import ControlledInputKind
def test_default_deny():
    r = evaluate_controlled_readonly_gate(Wave0ExecutionConfig(), Wave0AdapterKind.REPORT_READING, ControlledInputKind.SYNTHETIC)
    assert r.final == "DENY_DISABLED"
    assert "P0" in r.reason
def test_all_adapters_deny():
    for kind in Wave0AdapterKind:
        r = evaluate_controlled_readonly_gate(Wave0ExecutionConfig(), kind, ControlledInputKind.SYNTHETIC)
        assert r.final == "DENY_DISABLED"
