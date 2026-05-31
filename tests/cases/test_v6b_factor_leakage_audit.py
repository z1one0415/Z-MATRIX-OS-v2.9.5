import json
from pathlib import Path
W=Path(__file__).resolve().parent.parent.parent
def test_leakage():
    d=json.loads((W/"runtime_reports/cases/v6b_factor_leakage_audit.json").read_text())
    assert d["leakage_safe"] is True
    assert d["future_data_violations"]==0
    assert d["forward_return_as_factor_violations"]==0
    assert d["alpha_claim_violations"]==0
