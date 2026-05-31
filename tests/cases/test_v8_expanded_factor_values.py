import json
from pathlib import Path
W=Path(__file__).resolve().parent.parent.parent
def test():
    d=json.loads((W/"runtime_reports/cases/v8_expanded_factor_values.json").read_text())
    assert d["stock_count"]>=60
    assert d["as_of_date_count"]>=800
    for r in d["records"][:100]:
        assert r["ready_for_alpha_claim"] is False
        for f in r["factor_values"].values():
            assert f["uses_future_data"] is False
