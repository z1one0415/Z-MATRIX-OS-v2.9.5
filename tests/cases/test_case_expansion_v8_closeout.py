import json
from pathlib import Path
W=Path(__file__).resolve().parent.parent.parent
def test():
    d=json.loads((W/"runtime_reports/cases/case_expansion_v8_closeout.json").read_text())
    assert "CONFIRMED" in d["status"]
    assert d["stock_count"]>=60
    assert d["ready_for_alpha_claim"] is False
    assert d["alpha_validated"] is False
    assert d["production"]=="BLOCKED"
    assert d["buy_sell_instruction_count"]==0
