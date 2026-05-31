import json
from pathlib import Path
W=Path(__file__).resolve().parent.parent.parent
def test():
    d=json.loads((W/"runtime_reports/cases/v8_expanded_universe.json").read_text())
    assert d["stock_count"]>=60
    assert d["ready_for_alpha_claim"] is False
