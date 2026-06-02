import json
from pathlib import Path
W=Path(__file__).resolve().parent.parent.parent
def test():
    d=json.loads((W/"runtime_reports/cases/v11_5_portfolio_rules.json").read_text())
    assert d["portfolio_action"]=="PAPER_ONLY"
    assert d["investment_action"]=="NONE"
