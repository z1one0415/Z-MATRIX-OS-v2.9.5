import json
from pathlib import Path
W=Path(__file__).resolve().parent.parent.parent
def test():
    for fn in["v11_5_paper_portfolio_contract.json","v11_5_portfolio_rules.json","v11_5_paper_portfolio_simulation.json","v11_5_paper_portfolio_risk_audit.json","case_expansion_v11_5_closeout.json","v12_alpha_operating_loop_entry_gate.json"]:
        t=json.dumps(json.loads((W/"runtime_reports/cases"/fn).read_text())).upper()
        for w in["BUY","SELL","ADD","REDUCE"]:
            if w in t and"buy_sell"not in t.lower()and"forbidden"not in t.lower():assert False,f"{fn}:{w}"
