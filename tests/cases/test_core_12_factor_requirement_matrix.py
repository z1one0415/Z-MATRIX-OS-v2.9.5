import json
from pathlib import Path
W=Path(__file__).resolve().parent.parent.parent
def test_matrix():
    d=json.loads((W/"runtime_reports/cases/core_12_factor_requirement_matrix.json").read_text())
    assert d["core_12_cases"]==12
    for c in d["matrix"]:
        assert c["price_inputs_ready"] is True
        assert c["financial_inputs_ready"] is False
        assert c["valuation_inputs_ready"] is False
        assert c["ready_for_v6b_price_only_factor_calculation"] is True
        assert c["ready_for_alpha_claim"] is False
