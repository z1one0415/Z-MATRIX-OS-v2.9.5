import json
from pathlib import Path
W=Path(__file__).resolve().parent.parent.parent
def test_risk_fail_when_no_results():
    d=json.loads((W/"runtime_reports/cases/v11_5_paper_portfolio_risk_audit.json").read_text())
    assert d["status"]=="V11_5_PAPER_PORTFOLIO_RISK_AUDIT_FAIL"
    assert len(d["risk_violations"])>=3
    assert d["ready_for_v12"] is False
