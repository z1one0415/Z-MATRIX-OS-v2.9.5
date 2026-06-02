#!/usr/bin/env python3
"""V11.5-D: Evaluate benchmark and cost proxy."""
import json
from pathlib import Path
W=Path(__file__).resolve().parent.parent.parent;C=W/"runtime_reports"/"cases"
sim=json.loads((C/"v11_5_paper_portfolio_simulation.json").read_text())
gp=sum(1 for r in sim["results"]if r.get("bucket_spread")and r["bucket_spread"]>0)
np=sum(1 for r in sim["results"]if r.get("bucket_spread")and r["bucket_spread"]>0.003)
c={"status":"V11_5_BENCHMARK_COST_PROXY_EVALUATION_BUILT","cost_model_status":"PROXY_ONLY","one_way_cost_bps":15,"round_trip_cost_bps":30,"gross_positive_count":gp,"net_positive_count":np,"ready_for_alpha_claim":False,"alpha_validated":False,"production":"BLOCKED","broker_runtime":"BLOCKED","real_trade":"BLOCKED"}
json.dump(c,open(C/"v11_5_benchmark_cost_proxy_evaluation.json","w"),indent=2)
print(f"Cost: gross_pos={gp} net_pos={np}")
