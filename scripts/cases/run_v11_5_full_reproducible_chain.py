#!/usr/bin/env python3
"""Full chain — PASS requires closeout confirmed + V12 BLOCKED + safety."""
import subprocess,json
from pathlib import Path
W=Path(__file__).resolve().parent.parent.parent;C=W/"runtime_reports"/"cases"
S=["build_v11_5_paper_portfolio_contract.py","build_v11_5_portfolio_rules.py","select_v11_5_forward_compatible_as_of_date.py","build_v11_paper_signal_snapshot.py","audit_v11_5_forward_label_alignment.py","run_v11_5_paper_portfolio_simulation.py","evaluate_v11_5_benchmark_and_cost_proxy.py","audit_v11_5_paper_portfolio_risk.py","build_v11_5_closeout.py","check_v12_alpha_operating_loop_entry_gate.py"]
ok=True
for s in S:
    r=subprocess.run(["python3",str(W/"scripts/cases"/s)],cwd=str(W),capture_output=True,text=True)
    print(f"{'OK' if r.returncode==0 else 'FAIL'}: {s} {r.stdout.strip()[:80]}")
    if r.returncode!=0:ok=False
co=json.loads((C/"case_expansion_v11_5_closeout.json").read_text())
g=json.loads((C/"v12_alpha_operating_loop_entry_gate.json").read_text())
sim=json.loads((C/"v11_5_paper_portfolio_simulation.json").read_text())
closeout_confirmed=co.get("paper_portfolio_simulation_confirmed",False)
v12_blocked="BLOCKED"in g.get("status","")
v12_reasons=g.get("blocking_reasons",[])
v12_reasons_ok=all(r in v12_reasons for r in["PAPER_TRACKING_PERIOD_NOT_COMPLETED","COST_MODEL_PROXY_ONLY","NO_OUT_OF_SAMPLE_LIVE_TRACKING"])
safety_ok=co.get("production")=="BLOCKED"and co.get("broker_runtime")=="BLOCKED"and co.get("real_trade")=="BLOCKED"
alpha_ok=not co.get("ready_for_alpha_claim",True)and not co.get("alpha_validated",True)
hardgate=closeout_confirmed and v12_blocked and v12_reasons_ok and safety_ok and alpha_ok
chain_ok=ok and hardgate
status="V11_5_FULL_REPRODUCIBLE_CHAIN_PASS"if chain_ok else"V11_5_FULL_REPRODUCIBLE_CHAIN_BLOCKED"
r2={"status":status,"steps":S,"steps_returncode_pass":ok,"full_chain_hardgate_pass":hardgate,"closeout_confirmed":closeout_confirmed,"v12_gate_blocked":v12_blocked,"v12_reasons_present":v12_reasons_ok,"safety_blocked":safety_ok,"alpha_blocked":alpha_ok,"final_closeout_status":co["status"],"calculated_result_count":sim.get("calculated_result_count",0)}
json.dump(r2,open(C/"v11_5_full_reproducible_chain.json","w"),indent=2)
print(f"Full chain: {status} hardgate={hardgate} closeout={closeout_confirmed} v12_blocked={v12_blocked}")
