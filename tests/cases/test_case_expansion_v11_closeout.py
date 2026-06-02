import json
from pathlib import Path
W=Path(__file__).resolve().parent.parent.parent
def test():
    d=json.loads((W/"runtime_reports/cases/case_expansion_v11_closeout.json").read_text())
    assert "CONFIRMED" in d["status"]
    assert d["paper_trading_enabled"] is False
    assert d["production"]=="BLOCKED"
