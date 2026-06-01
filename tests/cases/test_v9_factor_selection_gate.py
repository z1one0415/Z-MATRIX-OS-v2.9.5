import json
from pathlib import Path
W=Path(__file__).resolve().parent.parent.parent
def test_selection():
    d=json.loads((W/"runtime_reports/cases/v9_factor_selection_gate.json").read_text())
    assert len(d["selection_results"])==80
    decisions={r["decision"] for r in d["selection_results"]}
    assert "PROMOTE_TO_COUNCIL_REVIEW" in decisions
    for r in d["selection_results"]:
        assert "BUY" not in r.get("decision","") and "SELL" not in r.get("decision","")
        assert r["alpha_validated"] is False
    assert d["alpha_validated"] is False
