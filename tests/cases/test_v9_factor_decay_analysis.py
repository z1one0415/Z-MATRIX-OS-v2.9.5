import json
from pathlib import Path
W=Path(__file__).resolve().parent.parent.parent
def test():
    d=json.loads((W/"runtime_reports/cases/v9_factor_decay_analysis.json").read_text())
    assert len(d["decay"])>=5
    assert d["alpha_validated"] is False
