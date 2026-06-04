import json
from pathlib import Path
import pytest
W = Path(__file__).resolve().parent.parent.parent
def test_gate_blocked_with_reasons():
    g = json.loads((W / "runtime_reports/cases/v12_alpha_operating_loop_entry_gate.json").read_text())
    assert g["status"] == "V12_ALPHA_OPERATING_LOOP_ENTRY_BLOCKED"
    assert g["ready_for_alpha_operating_loop"] is False
    assert "PAPER_TRACKING_PERIOD_NOT_COMPLETED" in g["blocking_reasons"]
def test_gate_no_alpha():
    g = json.loads((W / "runtime_reports/cases/v12_alpha_operating_loop_entry_gate.json").read_text())
    assert g["ready_for_alpha_claim"] is False
    assert g["alpha_validated"] is False
def test_gate_safety():
    g = json.loads((W / "runtime_reports/cases/v12_alpha_operating_loop_entry_gate.json").read_text())
    assert g["production"] == "BLOCKED"
    assert g["broker_runtime"] == "BLOCKED"
    assert g["real_trade"] == "BLOCKED"
