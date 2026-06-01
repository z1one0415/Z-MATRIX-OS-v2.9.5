import json
from pathlib import Path
W=Path(__file__).resolve().parent.parent.parent
def test_decay():
    d=json.loads((W/"runtime_reports/cases/v9_factor_decay_analysis.json").read_text())
    assert len(d["decay_results"])==16
    for r in d["decay_results"]:
        assert "decay_pattern" in r
        assert "rankic_by_horizon" in r
        assert "best_horizon" in r
        assert r["alpha_validated"] is False
    assert d["alpha_validated"] is False
