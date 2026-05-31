import json
from pathlib import Path
W=Path(__file__).resolve().parent.parent.parent
def test():
    g=json.loads((W/"runtime_reports/cases/v10_council_research_entry_gate.json").read_text())
    assert "ALLOWED" in g["status"]
    assert g["ready_for_alpha_claim"] is False
    assert g["production"]=="BLOCKED"
