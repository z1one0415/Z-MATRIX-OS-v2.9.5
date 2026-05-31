import json
from pathlib import Path
W=Path(__file__).resolve().parent.parent.parent
def test():
    d=json.loads((W/"runtime_reports/cases/v8_expanded_data_readiness.json").read_text())
    assert d["stock_count"]>=60
    assert d["price_coverage"]>=0.90
    assert d["ready_for_factor_rebuild"] is True
    assert d["ready_for_alpha_claim"] is False
