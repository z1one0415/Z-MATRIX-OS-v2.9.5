import json
from pathlib import Path
W = Path(__file__).resolve().parent.parent.parent
def test_benchmark_json():
    d = json.loads((W/"runtime_reports/cases/csi300_benchmark_returns.json").read_text())
    assert d["benchmark_id"] == "CSI300"
    for hk in ["T1","T5","T10","T20","T60"]:
        assert hk in d["returns"]
        assert d["returns"][hk]["truth_status"] == "REAL_READ_ONLY"
