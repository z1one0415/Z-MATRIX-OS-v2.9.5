import json
from pathlib import Path
W=Path(__file__).resolve().parent.parent.parent
def test():
    d=json.loads((W/"runtime_reports/cases/case_expansion_v11_5_closeout.json").read_text())
    assert d["status"]=="CASE_EXPANSION_V11_5_BLOCKED"
    assert d["label_alignment_pass"] is False
    assert d["calculated_result_count"]==0
    assert d["risk_audit_pass"] is False
    assert len(d["blocking_reasons"])>=3
