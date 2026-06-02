import json
from pathlib import Path
W=Path(__file__).resolve().parent.parent.parent
def test():
    d=json.loads((W/"runtime_reports/cases/v11_paper_signal_snapshot.json").read_text())
    assert d["candidate_factor_count"]>=10
    for s in d["snapshots"]:
        assert s["investment_action"]=="NONE"
        bp=s.get("bucket_policy","")
        assert bp.startswith("OBSERVATION_ONLY"),f"bucket_policy={bp}"
        if s.get("rankic_direction") in ("MIXED","MISSING"):
            assert s.get("favored_bucket_size",1)==0,f"MIXED favored_bucket_size should be 0"
