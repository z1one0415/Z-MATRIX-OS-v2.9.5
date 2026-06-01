#!/usr/bin/env python3
"""Run full V10 reproducible chain — requires closeout CONFIRMED for PASS."""
import subprocess, json
from pathlib import Path

W = Path(__file__).resolve().parent.parent.parent
STEPS = [
    "build_v10_council_input_pack.py",
    "run_v10_research_council_review.py",
    "run_v10_devil_advocate_review.py",
    "build_v10_candidate_factor_thesis_pack.py",
    "audit_v10_upstream_safety_alpha_fields.py",
    "check_v11_paper_watchlist_entry_gate.py",
    "build_v10_closeout.py",
]

steps_ok = True
for s in STEPS:
    r = subprocess.run(
        ["python3", str(W / "scripts" / "cases" / s)],
        cwd=str(W), capture_output=True, text=True,
    )
    status = "OK" if r.returncode == 0 else "FAIL"
    print(f"{status}: {s}  {r.stdout.strip()[:100]}")
    if r.returncode != 0:
        steps_ok = False

co = json.loads((W / "runtime_reports/cases/case_expansion_v10_closeout.json").read_text())
final_confirmed = (
    co.get("status") == "CASE_EXPANSION_V10_COUNCIL_RESEARCH_REVIEW_CONFIRMED"
    and co.get("blocking_reasons", ["X"]) == []
)
chain_ok = steps_ok and final_confirmed

result = {
    "status": "V10_FULL_REPRODUCIBLE_CHAIN_PASS" if chain_ok else "V10_FULL_REPRODUCIBLE_CHAIN_FAIL",
    "steps": STEPS,
    "steps_returncode_pass": steps_ok,
    "final_closeout_status": co["status"],
    "final_closeout_confirmed": final_confirmed,
    "upstream_safety_alpha_audit_pass": co.get("upstream_safety_alpha_audit_pass"),
    "ready_for_paper_watchlist": co.get("ready_for_paper_watchlist"),
    "blocking_reasons": co.get("blocking_reasons", []),
}
json.dump(
    result,
    open(W / "runtime_reports/cases/v10_full_reproducible_chain.json", "w"),
    indent=2,
)
print(
    f"Full chain: {'PASS' if chain_ok else 'FAIL'} "
    f"| scripts_ok={steps_ok} | confirmed={final_confirmed} "
    f"-> {co['status']}"
)
