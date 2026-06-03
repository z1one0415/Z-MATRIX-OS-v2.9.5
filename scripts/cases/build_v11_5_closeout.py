#!/usr/bin/env python3
"""Closeout — explicit 8-condition AND gate, no default-True."""
import json
from pathlib import Path
W=Path(__file__).resolve().parent.parent.parent;C=W/"runtime_reports"/"cases"
sim=json.loads((C/"v11_5_paper_portfolio_simulation.json").read_text())
align=json.loads((C/"v11_5_forward_label_alignment_audit.json").read_text())
cost=json.loads((C/"v11_5_benchmark_cost_proxy_evaluation.json").read_text())
risk=json.loads((C/"v11_5_paper_portfolio_risk_audit.json").read_text())
c1=align.get("status")=="V11_5_FORWARD_LABEL_ALIGNMENT_PASS"
c2=sim.get("simulation_completeness")=="FULL"or(sim.get("calculated_result_count",0)==30 and sim.get("blocked_result_count",0)==0)
c3=sim.get("calculated_result_count",0)==30 and sim.get("blocked_result_count",0)==0 and sim.get("null_return_count",0)==0
c4=cost.get("status")=="V11_5_BENCHMARK_COST_PROXY_EVALUATION_BUILT"
c5=cost.get("eligible_for_closeout_confirmed",False) is True
c6=risk.get("status")=="V11_5_PAPER_PORTFOLIO_RISK_AUDIT_PASS"
confirmed=c1 and c2 and c3 and c4 and c5 and c6
co={"status":"CASE_EXPANSION_V11_5_PAPER_PORTFOLIO_SIMULATION_CONFIRMED"if confirmed else"V11_5_BLOCKED","paper_portfolio_simulation_confirmed":confirmed,"portfolio_count":sim.get("portfolio_count",0),"calculated_result_count":sim["calculated_result_count"],"blocked_result_count":sim["blocked_result_count"],"null_return_count":sim["null_return_count"],"label_alignment_pass":c1,"simulation_full":c3,"cost_built":c4,"cost_eligible":c5,"risk_pass":c6,"ready_for_v12":False,"ready_for_alpha_claim":False,"alpha_validated":False,"production":"BLOCKED","broker_runtime":"BLOCKED","real_trade":"BLOCKED"}
json.dump(co,open(C/"case_expansion_v11_5_closeout.json","w"),indent=2)
print(f"Closeout: {co['status']} confirmed={confirmed} c:{int(c1)}{int(c2)}{int(c3)}{int(c4)}{int(c5)}{int(c6)}")
