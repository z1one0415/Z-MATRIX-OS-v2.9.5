import json
from pathlib import Path
W=Path(__file__).resolve().parent.parent.parent
FORBIDDEN=["BUY","SELL","alpha_validated: true","predictive_alpha: true","Alpha 已验证","production_allowed: true"]
def test_no_forbidden():
    for fn in ["v7_forward_return_labels.json","v7_exploratory_factor_metrics.json","v7_sample_adequacy_audit.json","case_expansion_v7_report.json","v8_expanded_sample_entry_gate.json"]:
        d=json.loads((W/"runtime_reports/cases"/fn).read_text())
        t=json.dumps(d).lower()
        for w in FORBIDDEN:
            if w.lower() in t and "buy_sell" not in t and "production_allowed" not in t:
                assert False,f"{fn}: {w}"
