import json
from pathlib import Path
W=Path(__file__).resolve().parent.parent.parent
def test_chain_blocked_status():
    d=json.loads((W/"runtime_reports/cases/v11_5_full_reproducible_chain.json").read_text())
    assert d["status"]=="V11_5_FULL_REPRODUCIBLE_CHAIN_BLOCKED"
    assert "audit_v11_5_forward_label_alignment" in str(d["steps"])
    assert d["label_alignment_pass"] is False
    assert d["calculated_result_count"]==0
    assert d["final_closeout_confirmed"] is False
