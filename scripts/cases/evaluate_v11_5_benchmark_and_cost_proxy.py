#!/usr/bin/env python3
"""Cost proxy evaluation — explicit eligibility fields."""
import json
from pathlib import Path
W=Path(__file__).resolve().parent.parent.parent;C=W/"runtime_reports"/"cases"
sim=json.loads((C/"v11_5_paper_portfolio_simulation.json").read_text())
calc=sim.get("calculated_result_count",0);blk=sim.get("blocked_result_count",0)
if calc==0:
    gp=None;np2=None;full=False
else:
    gp=sum(1 for r in sim["results"]if r.get("calculation_status")=="CALCULATED"and r.get("bucket_spread")is not None and r["bucket_spread"]>0)
    np2=sum(1 for r in sim["results"]if r.get("calculation_status")=="CALCULATED"and r.get("bucket_spread")is not None and r["bucket_spread"]>0.003)
    full=blk==0 and sim.get("null_return_count",0)==0
c={"status":"V11_5_BENCHMARK_COST_PROXY_EVALUATION_BUILT"if full else("V11_5_BENCHMARK_COST_PROXY_EVALUATION_BLOCKED"if calc==0 else"V11_5_BENCHMARK_COST_PROXY_EVALUATION_PARTIAL"),"gross_positive_count":gp,"net_positive_count":np2,"calculated_results_used":calc,"blocked_results_skipped":blk,"cost_model_status":"PROXY_ONLY","one_way_cost_bps":15,"round_trip_cost_bps":30,"eligible_for_closeout_confirmed":full,"eligible_for_v12":False,"ready_for_alpha_claim":False,"alpha_validated":False,"production":"BLOCKED","broker_runtime":"BLOCKED","real_trade":"BLOCKED"}
json.dump(c,open(C/"v11_5_benchmark_cost_proxy_evaluation.json","w"),indent=2)
print(f"Cost: {c['status']} eligible={full} gp={gp}")
