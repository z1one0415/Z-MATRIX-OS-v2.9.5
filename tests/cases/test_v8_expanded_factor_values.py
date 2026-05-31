import json
from pathlib import Path
W=Path(__file__).resolve().parent.parent.parent
def test_summary():
    d=json.loads((W/"runtime_reports/cases/v8_expanded_factor_values_summary.json").read_text())
    assert d["factor_values"]>=500000
    assert d["coverage"]>=0.95
    assert d["committed_to_git"] is False
