#!/usr/bin/env python3
"""Run V11 full reproducible chain with all hard gates."""
import subprocess, json
from pathlib import Path

W = Path(__file__).resolve().parent.parent.parent
C = W / "runtime_reports" / "cases"

STEPS = [
    "build_v11_paper_watchlist_contract.py",
    "build_v11_candidate_factor_watchlist.py",
    "build_v11_paper_signal_snapshot.py",
    "audit_v11_watchlist_semantics.py",
    "build_v11_paper_tracking_plan.py",
    "audit_v11_paper_watchlist.py",
    "build_v11_closeout.py",
    "check_v11_5_paper_portfolio_entry_gate.py",
]

steps_ok = True
for s in STEPS:
    r = subprocess.run(
        ["python3", str(W / "scripts" / "cases" / s)],
        cwd=str(W), capture_output=True, text=True,
    )
    print(
        f"{'OK' if r.returncode == 0 else 'FAIL'}: {s} "
        f"{r.stdout.strip()[:80]}"
    )
    if r.returncode != 0:
        steps_ok = False

sa = json.loads((C / "v11_watchlist_semantic_audit.json").read_text())
co = json.loads((C / "case_expansion_v11_closeout.json").read_text())
gate = json.loads((C / "v11_5_paper_portfolio_entry_gate.json").read_text())

sem_ok = sa.get("status") == "V11_WATCHLIST_SEMANTIC_AUDIT_PASS"
cl_ok = co.get("status") == "CASE_EXPANSION_V11_PAPER_WATCHLIST_CONFIRMED"
g_ok = "ALLOWED" in gate.get("status", "")
mv_ok = len(sa.get("mixed_bucket_violations", ["X"])) == 0
sv_ok = len(sa.get("snapshot_direction_violations", ["X"])) == 0

chain_ok = steps_ok and sem_ok and cl_ok and g_ok and mv_ok and sv_ok

result = {
    "status": "V11_FULL_REPRODUCIBLE_CHAIN_PASS" if chain_ok else "V11_FULL_REPRODUCIBLE_CHAIN_FAIL",
    "steps": STEPS,
    "steps_returncode_pass": steps_ok,
    "semantic_audit_pass": sem_ok,
    "mixed_bucket_violations": len(sa.get("mixed_bucket_violations", [])),
    "snapshot_direction_violations": len(sa.get("snapshot_direction_violations", [])),
    "final_closeout_status": co["status"],
    "final_closeout_confirmed": cl_ok,
    "v11_5_gate_status": gate["status"],
    "v11_5_gate_allowed": g_ok,
}
json.dump(
    result,
    open(C / "v11_full_reproducible_chain.json", "w"),
    indent=2,
)
print(
    f"Full chain: {'PASS' if chain_ok else 'FAIL'} "
    f"| closeout={cl_ok} gate={g_ok} sem={sem_ok} mv={mv_ok} sv={sv_ok}"
)
