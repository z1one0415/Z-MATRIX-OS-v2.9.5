#!/usr/bin/env python3
"""V11.5-D: Evaluate benchmark and cost proxy — fail-closed on missing data."""
import json
from pathlib import Path
W=Path(__file__).resolve().parent.parent.parent;C=W/"runtime_reports"/"cases"
sim=json.loads((C/"v11_5_paper_portfolio_simulation.json").read_text())
calc=sim.get("calculated_result_count",0);blocked=sim.get("blocked_result_count",0);nulls=sim.get("null_return_count",0);miss=sim.get("missing_label_count",0)
if calc==0 or blocked>0 or nulls>0:
    reasons=[] 
    if calc==0: reasons.append("NO_CALCULATED_PORTFOLIO_RESULTS")
    if blocked>0: reasons.append("BLOCKED_RESULTS_PRESENT")
    if nulls>0: reasons.append("NULL_RETURN_RESULTS_PRESENT")
    if miss>0: reasons.append("MISSING_FORWARD_LABELS")
    c={"status":"V11_5_BENCHMARK_COST_PROXY_EVALUATION_BLOCKED","blocking_reasons":reasons,"gross_positive_count":None,"net_positive_count":None,"cost_model_status":"PROXY_ONLY","one_way_cost_bps":15,"round_trip_cost_bps":30,"ready_for_alpha_claim":False,"alpha_validated":False,"production":"BLOCKED","broker_runtime":"BLOCKED","real_trade":"BLOCKED"}
else:
    gp=sum(1 for r in sim["results"]if r.get("bucket_spread")is not None and r["bucket_spread"]>0)
    np2=sum(1 for r in sim["results"]if r.get("bucket_spread")is not None and r["bucket_spread"]>0.003)
    c={"status":"V11_5_BENCHMARK_COST_PROXY_EVALUATION_BUILT","cost_model_status":"PROXY_ONLY","one_way_cost_bps":15,"round_trip_cost_bps":30,"gross_positive_count":gp,"net_positive_count":np2,"ready_for_alpha_claim":False,"alpha_validated":False,"production":"BLOCKED","broker_runtime":"BLOCKED","real_trade":"BLOCKED"}
json.dump(c,open(C/"v11_5_benchmark_cost_proxy_evaluation.json","w"),indent=2)
print(f"Cost: {c['status']} | gp={c.get('gross_positive_count')}")
