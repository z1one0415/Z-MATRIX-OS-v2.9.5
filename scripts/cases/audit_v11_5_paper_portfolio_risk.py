#!/usr/bin/env python3
"""V11.5-E: Audit paper portfolio risk — reads alignment, simulation, cost."""
import json
from pathlib import Path
W=Path(__file__).resolve().parent.parent.parent;C=W/"runtime_reports"/"cases"
sim=json.loads((C/"v11_5_paper_portfolio_simulation.json").read_text())
align=json.loads((C/"v11_5_forward_label_alignment_audit.json").read_text())
cost=json.loads((C/"v11_5_benchmark_cost_proxy_evaluation.json").read_text())
rv=[]
if not align.get("ready_for_portfolio_simulation"): rv.append("FORWARD_LABEL_ALIGNMENT_NOT_PASS")
if sim.get("calculated_result_count",0)==0: rv.append("NO_CALCULATED_PORTFOLIO_RESULTS")
if sim.get("blocked_result_count",0)>0: rv.append("BLOCKED_RESULTS_PRESENT")
if sim.get("null_return_count",0)>0: rv.append("NULL_RETURN_RESULTS_PRESENT")
if "BLOCKED"in cost.get("status",""): rv.append("COST_EVALUATION_BLOCKED")
ro=len(rv)==0
r={"status":"V11_5_PAPER_PORTFOLIO_RISK_AUDIT_PASS"if ro else"V11_5_PAPER_PORTFOLIO_RISK_AUDIT_FAIL","portfolio_items_checked":sim.get("portfolio_count",0),"risk_violations":rv,"investment_action_count":0,"ready_for_v12":False,"v12_blocking_reasons":["PAPER_TRACKING_PERIOD_NOT_COMPLETED","COST_MODEL_PROXY_ONLY","NO_OUT_OF_SAMPLE_LIVE_TRACKING"]}
json.dump(r,open(C/"v11_5_paper_portfolio_risk_audit.json","w"),indent=2)
print(f"Risk: {r['status']} | violations={rv}")
