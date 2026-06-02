import json
from pathlib import Path
W=Path(__file__).resolve().parent.parent.parent
def test(): 
    d=json.loads((W/"runtime_reports/cases/v11_paper_watchlist_contract.json").read_text())
    assert d["paper_trading_enabled"] is False
    assert d["portfolio_simulation_enabled"] is False
    assert d["production"]=="BLOCKED"
