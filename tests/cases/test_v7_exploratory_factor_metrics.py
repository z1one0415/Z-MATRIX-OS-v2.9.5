import json
from pathlib import Path
W=Path(__file__).resolve().parent.parent.parent
def test_metrics():
    d=json.loads((W/"runtime_reports/cases/v7_exploratory_factor_metrics.json").read_text())
    assert d["alpha_validated"] is False
    for m in d["metrics"]:
        assert m["alpha_validated"] is False
        assert m["sample_warning"]=="SMALL_SAMPLE_EXPLORATORY_ONLY"
