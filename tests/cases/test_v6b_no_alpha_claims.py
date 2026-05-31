import json
from pathlib import Path
W=Path(__file__).resolve().parent.parent.parent

def test_no_forbidden():
    files=["v6b_price_only_factor_values.json","v6b_factor_leakage_audit.json",
           "v6b_factor_coverage_audit.json","v6d_price_only_factor_closeout.json",
           "v7_factor_validation_entry_gate.json"]
    for fn in files:
        d=json.loads((W/"runtime_reports/cases"/fn).read_text())
        t=json.dumps(d).lower()
        if "buy" in t and "buy_sell_instruction_count" not in t: assert False, f"{fn}: BUY"
        if "sell" in t and "buy_sell_instruction_count" not in t: assert False, f"{fn}: SELL"
        for w in ["alpha_validated","predictive_alpha"]:
            assert w not in t, f"{fn}: {w}"
