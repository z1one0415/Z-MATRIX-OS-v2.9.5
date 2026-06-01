import json
from pathlib import Path
W=Path(__file__).resolve().parent.parent.parent
def test_robustness():
    d=json.loads((W/"runtime_reports/cases/v9_factor_robustness.json").read_text())
    assert len(d["robustness_results"])==16
    grades={"ROBUST","REVIEW","UNSTABLE","INSUFFICIENT"}
    for r in d["robustness_results"]:
        assert r["robustness_grade"] in grades
        assert "year_robustness" in r
        assert "regime_robustness" in r
        assert r["alpha_validated"] is False
