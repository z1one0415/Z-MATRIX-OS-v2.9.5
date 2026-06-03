#!/usr/bin/env python3
"""Risk audit — reads rules, scans forbidden actions."""
import json
from pathlib import Path
W=Path(__file__).resolve().parent.parent.parent;C=W/"runtime_reports"/"cases"
sim=json.loads((C/"v11_5_paper_portfolio_simulation.json").read_text())
align=json.loads((C/"v11_5_forward_label_alignment_audit.json").read_text())
cost=json.loads((C/"v11_5_benchmark_cost_proxy_evaluation.json").read_text())
rules=json.loads((C/"v11_5_portfolio_rules.json").read_text())
snap=json.loads((C/"v11_paper_signal_snapshot.json").read_text())
rv=[]
if not align.get("ready_for_portfolio_simulation"):rv.append("FORWARD_LABEL_ALIGNMENT_NOT_PASS")
if sim.get("calculated_result_count",0)==0:rv.append("NO_CALCULATED_RESULTS")
if sim.get("blocked_result_count",0)>0:rv.append("BLOCKED_RESULTS_PRESENT")
if sim.get("null_return_count",0)>0:rv.append("NULL_RETURNS")
if "BLOCKED"in cost.get("status",""):rv.append("COST_EVALUATION_BLOCKED")
def iv(obj):
    if isinstance(obj,dict):
        for v in obj.values():yield from iv(v)
    elif isinstance(obj,list):
        for it in obj:yield from iv(it)
    elif isinstance(obj,str):yield obj
FW=["BUY","SELL","ADD","REDUCE","\u4e70\u5165","\u5356\u51fa","\u5efa\u4ed3"]
fvs=[]
for doc in[sim,snap,rules]:
    for val in iv(doc):
        vu=val.upper()
        for w in FW:
            if w in vu and"INVESTMENT_ACTION_COUNT"not in vu and"buy_sell"not in vu.lower():fvs.append(w)
fvs=list(set(fvs))
if fvs:rv.append("FORBIDDEN_ACTION_DETECTED")
ro=len(rv)==0
r={"status":"V11_5_PAPER_PORTFOLIO_RISK_AUDIT_PASS"if ro else"V11_5_PAPER_PORTFOLIO_RISK_AUDIT_FAIL","portfolio_items_checked":sim.get("portfolio_count",0),"risk_violations":rv,"forbidden_action_violations":fvs,"investment_action_count":len(fvs),"ready_for_v12":False,"v12_blocking_reasons":["PAPER_TRACKING_PERIOD_NOT_COMPLETED","COST_MODEL_PROXY_ONLY","NO_OUT_OF_SAMPLE_LIVE_TRACKING"]}
json.dump(r,open(C/"v11_5_paper_portfolio_risk_audit.json","w"),indent=2)
print(f"Risk: {r['status']} violations={rv} forbid={fvs}")
