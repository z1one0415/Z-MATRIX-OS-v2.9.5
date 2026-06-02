import json
from pathlib import Path
W=Path(__file__).resolve().parent.parent.parent
def test():
    d=json.loads((W/"runtime_reports/cases/v11_candidate_factor_watchlist.json").read_text())
    for wi in d["watch_items"]:
        rd=wi["rankic_direction"]
        bu=wi["bucket_direction"]
        if rd=="NEGATIVE": assert "LOW" in bu
        elif rd=="POSITIVE": assert "HIGH" in bu
        elif rd=="MIXED": assert "NO_PREFERRED" in bu
