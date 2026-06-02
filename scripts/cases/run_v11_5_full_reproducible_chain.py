#!/usr/bin/env python3
"""Run V11.5 full reproducible chain."""
import subprocess,json
from pathlib import Path
W=Path(__file__).resolve().parent.parent.parent;C=W/"runtime_reports"/"cases"
STEPS=["build_v11_5_paper_portfolio_contract.py","build_v11_5_portfolio_rules.py","run_v11_5_paper_portfolio_simulation.py","evaluate_v11_5_benchmark_and_cost_proxy.py","audit_v11_5_paper_portfolio_risk.py","build_v11_5_closeout.py","check_v12_alpha_operating_loop_entry_gate.py"]
ok=True
for s in STEPS:
    r=subprocess.run(["python3",str(W/"scripts/cases"/s)],cwd=str(W),capture_output=True,text=True)
    print(f"{'OK' if r.returncode==0 else 'FAIL'}: {s} {r.stdout.strip()[:80]}")
    if r.returncode!=0:ok=False
co=json.loads((C/"case_expansion_v11_5_closeout.json").read_text())
g=json.loads((C/"v12_alpha_operating_loop_entry_gate.json").read_text())
final_ok=co.get("status")=="CASE_EXPANSION_V11_5_PAPER_PORTFOLIO_SIMULATION_CONFIRMED" and"BLOCKED"in g.get("status","")
chain_ok=ok and final_ok
r2={"status":"V11_5_FULL_REPRODUCIBLE_CHAIN_PASS"if chain_ok else"FAIL","steps":STEPS,"steps_returncode_pass":ok,"final_closeout_status":co["status"],"final_closeout_confirmed":co.get("status")=="CASE_EXPANSION_V11_5_PAPER_PORTFOLIO_SIMULATION_CONFIRMED","v12_gate_status":g["status"],"v12_gate_blocked":"BLOCKED"in g.get("status","")}
json.dump(r2,open(C/"v11_5_full_reproducible_chain.json","w"),indent=2)
print(f"Full chain: {'PASS' if chain_ok else 'FAIL'}")
