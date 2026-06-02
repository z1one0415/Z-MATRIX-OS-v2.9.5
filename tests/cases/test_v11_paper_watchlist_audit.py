import json
from pathlib import Path
W=Path(__file__).resolve().parent.parent.parent
def test():
    d=json.loads((W/"runtime_reports/cases/v11_paper_watchlist_audit.json").read_text())
    assert d["ready_for_v11_5"] is True
    assert d["investment_action_count"]==0
