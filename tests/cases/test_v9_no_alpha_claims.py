import json
from pathlib import Path
W=Path(__file__).resolve().parent.parent.parent
def test():
    for fn in ["v9_formal_factor_stability.json","v9_factor_decay_analysis.json","v9_factor_robustness.json","v9_factor_selection_gate.json","v10_council_research_entry_gate.json","case_expansion_v9_closeout.json"]:
        t=json.dumps(json.loads((W/"runtime_reports/cases"/fn).read_text())).lower()
        for w in ["buy","sell","alpha_validated: true","predictive_alpha"]:
            if w in t and "buy_sell" not in t: assert False,f"{fn}: {w}"
