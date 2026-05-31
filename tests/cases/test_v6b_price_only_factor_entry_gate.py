import json
from pathlib import Path
W=Path(__file__).resolve().parent.parent.parent
def test_gate():
    g=json.loads((W/"runtime_reports/cases/v6b_price_only_factor_entry_gate.json").read_text())
    assert "ALLOWED" in g["status"]
    assert g["ready_for_v6b_price_only_calculation"] is True
    assert g["ready_for_factor_validation"] is False
    assert g["ready_for_alpha_claim"] is False
    assert g["synthetic_factor_allowed_count"]==0
    assert g["production"]=="BLOCKED"

def test_gate_aligned_with_closeout():
    g=json.loads((W/"runtime_reports/cases/v6b_price_only_factor_entry_gate.json").read_text())
    co=json.loads((W/"runtime_reports/cases/case_expansion_v6a_closeout.json").read_text())
    assert g["price_only_factor_ready_count"]==co["v6b_calculable_history_factors"]
