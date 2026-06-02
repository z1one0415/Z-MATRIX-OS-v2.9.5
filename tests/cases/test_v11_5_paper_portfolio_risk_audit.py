import json
from pathlib import Path
W=Path(__file__).resolve().parent.parent.parent
def test():
    d=json.loads((W/"runtime_reports/cases/v11_5_paper_portfolio_risk_audit.json").read_text())
    assert d["ready_for_v12"] is False
    assert len(d["v12_blocking_reasons"])>=2
