import json
from pathlib import Path
W=Path(__file__).resolve().parent.parent.parent
def test():
    d=json.loads((W/"runtime_reports/cases/v9_factor_robustness.json").read_text())
    assert len(d["robustness"])>=5
    assert d["alpha_validated"] is False
