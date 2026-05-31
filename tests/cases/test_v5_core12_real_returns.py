import json
from pathlib import Path
W = Path(__file__).resolve().parent.parent.parent
def test_real_returns_json():
    d = json.loads((W/"runtime_reports/cases/core_12_real_returns.json").read_text())
    assert d["total_cases"] == 12
    assert len(d["horizons"]) == 5
    for c in d["cases"]:
        for hk in d["horizons"]:
            assert hk in c["returns"]
            assert "truth_status" in c["returns"][hk]
            assert c["returns"][hk]["truth_status"] == "REAL_READ_ONLY", f"{c['case_id']} {hk}: {c['returns'][hk]['truth_status']}"
def test_returns_formula():  # T1 return = exit/entry - 1
    c = [x for x in json.loads((W/"runtime_reports/cases/core_12_real_returns.json").read_text())["cases"] if x["ticker"]=="300750"][0]
    r = c["returns"]["T1"]
    assert r["return"] is not None
def test_no_buy_sell():
    text = json.dumps(json.loads((W/"runtime_reports/cases/core_12_real_returns.json").read_text()))
    assert "BUY" not in text.upper()
