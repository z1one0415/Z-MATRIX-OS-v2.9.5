#!/usr/bin/env python3
"""V12-Prep Full Chain Runner — runs all sub-stages and V12 gate."""
import subprocess, json
from pathlib import Path

W = Path(__file__).resolve().parent.parent.parent
C = W / "runtime_reports" / "cases"

STEPS = [
    "build_v11_6_closeout.py", "build_v11_7_closeout.py",
    "build_v11_8_closeout.py", "build_v11_9_closeout.py",
    "check_v12_alpha_operating_loop_entry_gate.py","build_v12_entry_gate_recheck_report.py",
    "check_v12_alpha_operating_loop_entry_gate.py",
]

ok = True
for s in STEPS:
    r = subprocess.run(
        ["python3", str(W / "scripts" / "cases" / s)],
        cwd=str(W), capture_output=True, text=True,
    )
    print(f"{'OK' if r.returncode == 0 else 'FAIL'}: {s} {r.stdout.strip()[:80]}")
    if r.returncode != 0:
        ok = False

g = json.loads((C / "v12_alpha_operating_loop_entry_gate.json").read_text())
blocked = "BLOCKED" in g.get("status", "")
has_reasons = len(g.get("blocking_reasons", [])) > 0
gate_consistent = (blocked and has_reasons) or (not blocked and not has_reasons)
chain_ok = ok and gate_consistent

r = {
    "status": "V12_PREP_FULL_REPRODUCIBLE_CHAIN_PASS" if chain_ok else "V12_PREP_FULL_REPRODUCIBLE_CHAIN_BLOCKED",
    "steps_returncode_pass": ok,
    "gate_logic_consistent": gate_consistent,
    "v12_gate_status": g["status"],
    "v12_gate_blocked_or_research_only": True,
    "blocking_reasons": g.get("blocking_reasons", []),
    "ready_for_alpha_claim": False,
    "alpha_validated": False,
    "production": "BLOCKED",
    "broker_runtime": "BLOCKED",
    "real_trade": "BLOCKED",
}
json.dump(r, open(C / "v12_prep_full_reproducible_chain.json", "w"), indent=2)
print(f"V12-Prep Chain: {r['status']} gate_consistent={gate_consistent}")
