import json
from pathlib import Path
W=Path(__file__).resolve().parent.parent.parent
def test_adequacy():
    d=json.loads((W/"runtime_reports/cases/v7_sample_adequacy_audit.json").read_text())
    assert d["horizon_status"]["T60"]=="INSUFFICIENT"
    assert d["formal_validation_allowed"] is False
    assert d["alpha_claim_allowed"] is False
