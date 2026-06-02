import json
from pathlib import Path
W=Path(__file__).resolve().parent.parent.parent
def test():
    d=json.loads((W/"runtime_reports/cases/v11_paper_signal_snapshot.json").read_text())
    assert d["candidate_factor_count"]>=10
    for s in d["snapshots"]:
        assert s["investment_action"]=="NONE"
        assert s["bucket_policy"]=="OBSERVATION_ONLY_NO_TRADE"
