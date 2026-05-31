import json
from pathlib import Path
W = Path(__file__).resolve().parent.parent.parent
def test_relative_returns():
    d = json.loads((W/"runtime_reports/cases/core_12_benchmark_relative_returns.json").read_text())
    assert len(d["cases"]) == 12
    for c in d["cases"]:
        for hk in d["horizons"]:
            assert c["relative_returns"][hk]["can_interpret_as_predictive_alpha"] is False
def test_alpha_claim_false():
    for c in json.loads((W/"runtime_reports/cases/core_12_benchmark_relative_returns.json").read_text())["cases"]:
        assert c["ready_for_alpha_claim"] is False
def test_formula():
    c002 = [c for c in json.loads((W/"runtime_reports/cases/core_12_benchmark_relative_returns.json").read_text())["cases"] if c["ticker"]=="300750"][0]
    rr = c002["relative_returns"]["T20"]
    if rr["stock_return"] is not None and rr["benchmark_return"] is not None:
        assert abs(rr["benchmark_relative_return"] - (rr["stock_return"] - rr["benchmark_return"])) < 0.001
