import json
from pathlib import Path
W=Path(__file__).resolve().parent.parent.parent

def test_gate_research_only_allowed():
    """V12 gate is RESEARCH_ONLY_ALLOWED with 0 blocking reasons."""
    g=json.loads((W/"runtime_reports/cases/v12_alpha_operating_loop_entry_gate.json").read_text())
    assert g["status"]=="V12_ALPHA_OPERATING_LOOP_RESEARCH_ONLY_ALLOWED"
    assert g["research_only"] is True
    assert g["ready_for_alpha_operating_loop"] is True
    assert g["blocking_reasons"]==[]
    assert g["ready_for_alpha_claim"] is False
    assert g["alpha_validated"] is False

def test_gate_safety_always_blocked():
    """Safety channels remain blocked regardless of gate status."""
    g=json.loads((W/"runtime_reports/cases/v12_alpha_operating_loop_entry_gate.json").read_text())
    assert g["production"]=="BLOCKED"
    assert g["broker_runtime"]=="BLOCKED"
    assert g["real_trade"]=="BLOCKED"
