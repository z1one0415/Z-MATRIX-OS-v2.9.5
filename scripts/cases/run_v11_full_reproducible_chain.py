#!/usr/bin/env python3
"""Run V11 full reproducible chain."""
import subprocess,json
from pathlib import Path
W=Path(__file__).resolve().parent.parent.parent; C=W/"runtime_reports"/"cases"
STEPS=["build_v11_paper_watchlist_contract.py","build_v11_candidate_factor_watchlist.py","build_v11_paper_signal_snapshot.py","build_v11_paper_tracking_plan.py","audit_v11_paper_watchlist.py","build_v11_closeout.py","check_v11_5_paper_portfolio_entry_gate.py"]
ok=True
for s in STEPS:
    r=subprocess.run(["python3",str(W/"scripts/cases"/s)],cwd=str(W),capture_output=True,text=True)
    print(f"{'OK' if r.returncode==0 else 'FAIL'}: {s} {r.stdout.strip()[:80]}")
    if r.returncode!=0: ok=False
co=json.loads((C/"case_expansion_v11_closeout.json").read_text())
final_ok=co.get("status")=="CASE_EXPANSION_V11_PAPER_WATCHLIST_CONFIRMED"
chain_ok=ok and final_ok
r={"status":"V11_FULL_REPRODUCIBLE_CHAIN_PASS" if chain_ok else"FAIL","steps":STEPS,"steps_returncode_pass":ok,"final_closeout_status":co["status"],"final_closeout_confirmed":final_ok}
json.dump(r,open(C/"v11_full_reproducible_chain.json","w"),indent=2)
print(f"Full chain: {'PASS' if chain_ok else 'FAIL'}")
