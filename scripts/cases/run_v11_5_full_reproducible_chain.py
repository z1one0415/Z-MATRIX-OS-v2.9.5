#!/usr/bin/env python3
"""V11.5 Full Chain — with partial state awareness."""
import subprocess,json
from pathlib import Path
W=Path(__file__).resolve().parent.parent.parent;C=W/"runtime_reports"/"cases"
S=["build_v11_5_paper_portfolio_contract.py","build_v11_5_portfolio_rules.py",
   "select_v11_5_forward_compatible_as_of_date.py","build_v11_paper_signal_snapshot.py",
   "audit_v11_5_forward_label_alignment.py","run_v11_5_paper_portfolio_simulation.py",
   "evaluate_v11_5_benchmark_and_cost_proxy.py","audit_v11_5_paper_portfolio_risk.py",
   "build_v11_5_closeout.py","check_v12_alpha_operating_loop_entry_gate.py"]
ok=True
for s in S:
    r=subprocess.run(["python3",str(W/"scripts/cases"/s)],cwd=str(W),capture_output=True,text=True)
    print(f"{'OK' if r.returncode==0 else 'FAIL'}: {s} {r.stdout.strip()[:80]}")
    if r.returncode!=0:ok=False
co=json.loads((C/"case_expansion_v11_5_closeout.json").read_text())
sim=json.loads((C/"v11_5_paper_portfolio_simulation.json").read_text())
g=json.loads((C/"v12_alpha_operating_loop_entry_gate.json").read_text())
is_partial=co.get("status")=="CASE_EXPANSION_V11_5_BLOCKED_PARTIAL_RESULTS"
is_confirmed=co.get("status")=="CASE_EXPANSION_V11_5_PAPER_PORTFOLIO_SIMULATION_CONFIRMED"
chain_status="V11_5_FULL_REPRODUCIBLE_CHAIN_PASS"if(is_confirmed and ok)else("V11_5_FULL_REPRODUCIBLE_CHAIN_BLOCKED_PARTIAL"if(is_partial and ok)else"V11_5_FULL_REPRODUCIBLE_CHAIN_BLOCKED")
r2={"status":chain_status,"steps":S,"steps_returncode_pass":ok,"final_closeout_status":co["status"],"final_closeout_confirmed":is_confirmed,"partial_results_available":is_partial,"partial_results_usable_for_report":co.get("partial_results_usable_for_report",is_partial),"partial_results_eligible_for_v12":False,"calculated_result_count":sim.get("calculated_result_count",0),"blocked_result_count":sim.get("blocked_result_count",0),"v12_gate_status":g["status"]}
json.dump(r2,open(C/"v11_5_full_reproducible_chain.json","w"),indent=2)
print(f"Full chain: {chain_status} | partial={is_partial} confirmed={is_confirmed}")
