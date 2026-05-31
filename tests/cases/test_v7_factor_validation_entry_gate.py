import json
from pathlib import Path
W=Path(__file__).resolve().parent.parent.parent
def test_gate():
    g=json.loads((W/"runtime_reports/cases/v7_factor_validation_entry_gate.json").read_text())
    assert "ALLOWED" in g["status"]
    assert g["ready_for_v7_factor_validation"] is True
    assert g["ready_for_alpha_claim"] is False
    assert g["production"]=="BLOCKED"
