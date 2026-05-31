import json
from pathlib import Path
W=Path(__file__).resolve().parent.parent.parent
def test_values():
    d=json.loads((W/"runtime_reports/cases/v6b_price_only_factor_values.json").read_text())
    assert d["factor_count"]==16
    assert d["core_12_cases"]==12
    assert d["as_of_date_count"]>=40
    assert d["lookback_policy"]=="TRAILING_ONLY_NO_FUTURE_DATA"
    for r in d["records"]:
        assert r["ready_for_alpha_claim"] is False
        for f in r["factor_values"].values():
            assert f["uses_future_data"] is False
def test_no_forward_factor_ids():
    d=json.loads((W/"runtime_reports/cases/v6b_price_only_factor_values.json").read_text())
    for r in d["records"]:
        for fid in r["factor_values"]:
            for fb in ["FORWARD_RETURN","FUTURE_RETURN","FWD_RETURN"]:
                assert fb not in fid.upper()
def test_drawdown_non_positive():
    d=json.loads((W/"runtime_reports/cases/v6b_price_only_factor_values.json").read_text())
    for r in d["records"]:
        if "MAX_DRAWDOWN_60D" in r["factor_values"]:
            v=r["factor_values"]["MAX_DRAWDOWN_60D"]["value"]
            assert v<=0, f"{r['ticker']}@{r['as_of_date']}: DD={v}"
