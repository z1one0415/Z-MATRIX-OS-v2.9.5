import json
from pathlib import Path
W=Path(__file__).resolve().parent.parent.parent
def test_factor_script_not_empty():
    t=(W/"scripts/cases/calculate_v8_expanded_price_only_factors.py").read_text()
    assert len(t)>500 and "print" not in t.split("\n")[0].lower()
    assert "v8_expanded_daily_price_bar.csv" in t
def test_labels_script_not_empty():
    t=(W/"scripts/cases/build_v8_forward_return_labels.py").read_text()
    assert len(t)>500
    assert "v8_expanded_daily_price_bar.csv" in t
def test_gate_script_not_empty():
    t=(W/"scripts/cases/check_v9_formal_factor_validation_entry_gate.py").read_text()
    assert len(t)>200
    assert "v8_factor_leakage_audit.json" in t
def test_v9_gate_allowed():
    g=json.loads((W/"runtime_reports/cases/v9_formal_factor_validation_entry_gate.json").read_text())
    assert "ALLOWED" in g["status"]
    assert g["ready_for_alpha_claim"] is False
