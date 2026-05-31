import json
from pathlib import Path
W=Path(__file__).resolve().parent.parent.parent
def test():
    d=json.loads((W/"runtime_reports/cases/v8_expanded_data_readiness.json").read_text())
    assert d["data_ready_count"]>=60
    assert d["universe_target_count"]==72
    assert d["universe_gap_count"]==1
    assert d["price_coverage"]>=0.90
    assert d["ready_for_factor_rebuild"] is True
    assert d["ready_for_alpha_claim"] is False
    assert "universe_gap_explanation" in d
