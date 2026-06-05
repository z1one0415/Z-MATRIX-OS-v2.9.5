import json
from pathlib import Path
W=Path(__file__).resolve().parent.parent.parent

def test_gate_research_only_allowed_no_reasons():
    """Gate is RESEARCH_ONLY_ALLOWED — zero blocking reasons."""
    g=json.loads((W/"runtime_reports/cases/v12_alpha_operating_loop_entry_gate.json").read_text())
    assert g["status"]=="V12_ALPHA_OPERATING_LOOP_RESEARCH_ONLY_ALLOWED"
    assert g["blocking_reasons"]==[]
    assert g["research_only"] is True
    assert g["ready_for_alpha_operating_loop"] is True

def test_gate_no_alpha():
    g=json.loads((W/"runtime_reports/cases/v12_alpha_operating_loop_entry_gate.json").read_text())
    assert g["ready_for_alpha_claim"] is False
    assert g["alpha_validated"] is False

def test_gate_safety():
    g=json.loads((W/"runtime_reports/cases/v12_alpha_operating_loop_entry_gate.json").read_text())
    assert g["production"]=="BLOCKED"

def test_research_only_false_when_blocked():
    """Semantic guard: research_only must be false when gate is BLOCKED."""
    g=json.loads((W/"runtime_reports/cases/v12_alpha_operating_loop_entry_gate.json").read_text())
    if "BLOCKED" in g["status"]:
        assert g["research_only"] is False
        assert g["ready_for_alpha_operating_loop"] is False
    else:
        # Gate is ALLOWED → research_only must be true
        assert g["research_only"] is True

def test_chain_semantic_fields():
    c=json.loads((W/"runtime_reports/cases/v12_prep_full_reproducible_chain.json").read_text())
    assert c["gate_logic_consistent"] is True
    assert c["gate_ready_semantics_ok"] is True
    assert c["gate_research_only_semantics_ok"] is True
    assert c["safety_blocked"] is True
