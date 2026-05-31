import json
from pathlib import Path
W=Path(__file__).resolve().parent.parent.parent
def test():
    for fn in ["v8_expanded_universe.json","v8_expanded_data_readiness.json","v8_expanded_factor_values.json","v8_factor_leakage_audit.json","v8_forward_return_labels.json","v8_sample_adequacy_audit.json","v9_formal_factor_validation_entry_gate.json","case_expansion_v8_closeout.json"]:
        t=json.dumps(json.loads((W/"runtime_reports/cases"/fn).read_text())).lower()
        for w in ["buy","sell","alpha_validated: true","predictive_alpha: true"]:
            if w in t and "buy_sell" not in t: assert False,f"{fn}: {w}"
