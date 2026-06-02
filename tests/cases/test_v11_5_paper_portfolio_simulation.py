import json
from pathlib import Path
W=Path(__file__).resolve().parent.parent.parent
def test():
    d=json.loads((W/"runtime_reports/cases/v11_5_paper_portfolio_simulation.json").read_text())
    for r in d["results"]:
        assert r["paper_only"] is True
        assert r["investment_action"]=="NONE"
