import json
from pathlib import Path
W=Path(__file__).resolve().parent.parent.parent
def test():
    g=json.loads((W/"runtime_reports/cases/v12_alpha_operating_loop_entry_gate.json").read_text())
    assert "BLOCKED" in g["status"]
    assert g["ready_for_alpha_operating_loop"] is False
    assert "V11_5_NOT_CONFIRMED" in g["blocking_reasons"]
    assert "FORWARD_LABEL_ALIGNMENT_NOT_PASS" in g.get("blocking_reasons",[])
