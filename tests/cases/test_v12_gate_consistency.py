import json
from pathlib import Path
W=Path(__file__).resolve().parent.parent.parent
def test_gate_blocked_with_reasons():
    g=json.loads((W/"runtime_reports/cases/v12_alpha_operating_loop_entry_gate.json").read_text())
    assert g["status"]=="V12_ALPHA_OPERATING_LOOP_ENTRY_BLOCKED"
    assert "PAPER_TRACKING_PERIOD_NOT_COMPLETED" in g["blocking_reasons"]
def test_gate_no_alpha():
    g=json.loads((W/"runtime_reports/cases/v12_alpha_operating_loop_entry_gate.json").read_text())
    assert g["ready_for_alpha_claim"] is False
    assert g["alpha_validated"] is False
def test_gate_safety():
    g=json.loads((W/"runtime_reports/cases/v12_alpha_operating_loop_entry_gate.json").read_text())
    assert g["production"]=="BLOCKED"
def test_research_only_false_when_blocked():
    g=json.loads((W/"runtime_reports/cases/v12_alpha_operating_loop_entry_gate.json").read_text())
    if g["status"]=="V12_ALPHA_OPERATING_LOOP_ENTRY_BLOCKED":
        assert g["research_only"] is False
        assert g["ready_for_alpha_operating_loop"] is False
def test_chain_semantic_fields():
    c=json.loads((W/"runtime_reports/cases/v12_prep_full_reproducible_chain.json").read_text())
    assert c["gate_logic_consistent"] is True
    assert c["gate_ready_semantics_ok"] is True
    assert c["gate_research_only_semantics_ok"] is True
    assert c["safety_blocked"] is True
