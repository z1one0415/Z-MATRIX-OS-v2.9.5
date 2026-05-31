import json
from pathlib import Path
W=Path(__file__).resolve().parent.parent.parent
def test_gate():
    g=json.loads((W/"runtime_reports/cases/v8_expanded_sample_entry_gate.json").read_text())
    assert g["ready_for_alpha_claim"] is False
    assert g["production"]=="BLOCKED"
