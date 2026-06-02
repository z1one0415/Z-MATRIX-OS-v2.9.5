import json
from pathlib import Path
W=Path(__file__).resolve().parent.parent.parent
def test():
    d=json.loads((W/"runtime_reports/cases/v11_candidate_factor_watchlist.json").read_text())
    assert d["watch_items_count"]>=10
    for wi in d["watch_items"]:
        assert "rankic_direction" in wi
        assert wi["investment_action"]=="NONE"
        assert wi["decay_pattern_basis"] is not None
        assert wi["raw_rankic_trend"] is not None
