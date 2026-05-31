import json
from pathlib import Path
W=Path(__file__).resolve().parent.parent.parent
def test():
    d=json.loads((W/"runtime_reports/cases/v8_factor_coverage_audit.json").read_text())
    assert d["coverage"]>=0.90
