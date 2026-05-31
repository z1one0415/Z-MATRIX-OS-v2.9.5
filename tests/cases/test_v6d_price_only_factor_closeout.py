import json
from pathlib import Path
W=Path(__file__).resolve().parent.parent.parent
def test_closeout():
    d=json.loads((W/"runtime_reports/cases/v6d_price_only_factor_closeout.json").read_text())
    assert "CONFIRMED" in d["status"]
    assert d["leakage_audit_pass"] is True
    assert d["coverage_audit_pass"] is True
    assert d["factor_records"]>=10000
    assert d["ready_for_factor_validation"] is False
    assert d["ready_for_v7_validation_entry"] is True
    assert d["alpha_claim_count"]==0
    assert d["production"]=="BLOCKED"
