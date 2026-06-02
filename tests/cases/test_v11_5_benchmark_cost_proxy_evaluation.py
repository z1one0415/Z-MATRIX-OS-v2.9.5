import json
from pathlib import Path
W=Path(__file__).resolve().parent.parent.parent
def test_cost_blocked_when_no_results():
    d=json.loads((W/"runtime_reports/cases/v11_5_benchmark_cost_proxy_evaluation.json").read_text())
    assert d["status"]=="V11_5_BENCHMARK_COST_PROXY_EVALUATION_BLOCKED"
    assert d["gross_positive_count"] is None
    assert len(d["blocking_reasons"])>=2
