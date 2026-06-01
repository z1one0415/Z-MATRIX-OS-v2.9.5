#!/usr/bin/env python3
"""Run full V10 reproducible chain in order."""
import subprocess, json
from pathlib import Path
W=Path(__file__).resolve().parent.parent.parent
steps=[
    "build_v10_council_input_pack.py",
    "run_v10_research_council_review.py",
    "run_v10_devil_advocate_review.py",
    "build_v10_candidate_factor_thesis_pack.py",
    "audit_v10_upstream_safety_alpha_fields.py",
    "check_v11_paper_watchlist_entry_gate.py",
    "build_v10_closeout.py",
]
ok=True
for s in steps:
    r=subprocess.run(["python3",str(W/"scripts/cases"/s)],cwd=str(W),capture_output=True,text=True)
    print(f"{'OK' if r.returncode==0 else 'FAIL'}: {s}  {r.stdout.strip()[:80]}")
    if r.returncode!=0: ok=False
co=json.loads((W/"runtime_reports/cases/case_expansion_v10_closeout.json").read_text())
result=dict(status="V10_FULL_REPRODUCIBLE_CHAIN_PASS" if ok else "V10_FULL_REPRODUCIBLE_CHAIN_FAIL",steps=steps,final_closeout_status=co["status"])
json.dump(result,open(W/"runtime_reports/cases/v10_full_reproducible_chain.json","w"),indent=2)
print(f"Full chain: {'PASS' if ok else 'FAIL'} -> {co['status']}")
