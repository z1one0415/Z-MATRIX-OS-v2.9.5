import json
from pathlib import Path
W=Path(__file__).resolve().parent.parent.parent
def test():
    d=json.loads((W/"runtime_reports/cases/v8_factor_leakage_audit.json").read_text())
    assert d["leakage_safe"] is True
    assert d["future_data_violations"]==0
