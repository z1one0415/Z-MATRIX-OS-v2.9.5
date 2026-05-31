import json
from pathlib import Path
W=Path(__file__).resolve().parent.parent.parent
def test_coverage():
    d=json.loads((W/"runtime_reports/cases/v6b_factor_coverage_audit.json").read_text())
    assert d["coverage"]>=0.95
    assert d["expected_records"]==10944
    assert d["valid_records"]>=10400
    for f,v in d["coverage_by_factor"].items():
        assert v>=0.95,f"Factor {f} coverage={v}"
    for t,v in d["coverage_by_ticker"].items():
        assert v>=0.95,f"Ticker {t} coverage={v}"
