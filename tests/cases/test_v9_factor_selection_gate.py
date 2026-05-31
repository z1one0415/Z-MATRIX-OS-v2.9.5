import json
from pathlib import Path
W=Path(__file__).resolve().parent.parent.parent
def test():
    d=json.loads((W/"runtime_reports/cases/v9_factor_selection_gate.json").read_text())
    assert d["promoted_count"]>=1
    assert d["alpha_validated"] is False
    for p in d["promoted"]:
        assert p["grade"]=="PROMOTE_TO_COUNCIL_REVIEW"
        assert "BUY" not in p["grade"] and "SELL" not in p["grade"]
