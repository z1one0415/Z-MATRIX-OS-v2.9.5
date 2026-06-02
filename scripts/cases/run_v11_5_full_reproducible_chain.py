#!/usr/bin/env python3
"""V11.5 Full Chain — with forward label alignment audit + fail-closed status."""
import subprocess,json
from pathlib import Path
W=Path(__file__).resolve().parent.parent.parent;C=W/"runtime_reports"/"cases"
S=["build_v11_5_paper_portfolio_contract.py","build_v11_5_portfolio_rules.py",
   "audit_v11_5_forward_label_alignment.py","run_v11_5_paper_portfolio_simulation.py",
   "evaluate_v11_5_benchmark_and_cost_proxy.py","audit_v11_5_paper_portfolio_risk.py",
   "build_v11_5_closeout.py","check_v12_alpha_operating_loop_entry_gate.py"]
ok=True
for s in S:
    r=subprocess.run(["python3",str(W/"scripts/cases"/s)],cwd=str(W),capture_output=True,text=True)
    print(f"{"OK" if r.returncode==0 else "FAIL"}: {s} {r.stdout.strip()[:80]}")
    if r.returncode!=0:ok=False
sim=json.loads((C/"v11_5_paper_portfolio_simulation.json").read_text())
align=json.loads((C/"v11_5_forward_label_alignment_audit.json").read_text())
co=json.loads((C/"case_expansion_v11_5_closeout.json").read_text())
risk=json.loads((C/"v11_5_paper_portfolio_risk_audit.json").read_text())
cost=json.loads((C/"v11_5_benchmark_cost_proxy_evaluation.json").read_text())
g=json.loads((C/"v12_alpha_operating_loop_entry_gate.json").read_text())
final_ok=(align.get("ready_for_portfolio_simulation")and sim.get("calculated_result_count",0)>0
    and sim.get("blocked_result_count",0)==0 and sim.get("null_return_count",0)==0
    and co.get("status")=="CASE_EXPANSION_V11_5_PAPER_PORTFOLIO_SIMULATION_CONFIRMED"
    and "BLOCKED"in g.get("status",""))
chain_ok=ok and final_ok
r2={"status":"V11_5_FULL_REPRODUCIBLE_CHAIN_PASS"if chain_ok else"V11_5_FULL_REPRODUCIBLE_CHAIN_BLOCKED",
    "steps":S,"steps_returncode_pass":ok,"label_alignment_pass":align.get("ready_for_portfolio_simulation"),
    "calculated_result_count":sim.get("calculated_result_count",0),
    "blocked_result_count":sim.get("blocked_result_count",0),
    "null_return_count":sim.get("null_return_count",0),
    "cost_evaluation_status":cost.get("status",""),
    "risk_audit_status":risk.get("status",""),
    "final_closeout_status":co.get("status",""),
    "final_closeout_confirmed":co.get("status")=="CASE_EXPANSION_V11_5_PAPER_PORTFOLIO_SIMULATION_CONFIRMED",
    "v12_gate_status":g.get("status","")}
json.dump(r2,open(C/"v11_5_full_reproducible_chain.json","w"),indent=2)
print(f"Full chain: {r2["status"]} | label_ok={align.get("ready_for_portfolio_simulation")} calc={sim.get("calculated_result_count",0)}")
