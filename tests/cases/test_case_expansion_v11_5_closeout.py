import json
from pathlib import Path
W=Path(__file__).resolve().parent.parent.parent
def test():
    d=json.loads((W/"runtime_reports/cases/case_expansion_v11_5_closeout.json").read_text())
    assert "CONFIRMED" in d["status"]
    assert d["ready_for_v12"] is False
    assert d["ready_for_alpha_claim"] is False
    assert d["production"]=="BLOCKED"
