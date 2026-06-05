#!/usr/bin/env python3
"""V12.1: Live Paper Full Chain Runner — orchestrates V12 base → V12.1 contract→registry→schedule→status→delta→audit→closeout."""
import subprocess
import json
from pathlib import Path

W = Path(__file__).resolve().parent.parent.parent
C = W / "runtime_reports" / "cases"

STEPS = [
    # V12.0 base (re-run to ensure consistency)
    "run_v12_research_only_full_chain.py",
    # V12.1 layer
    "build_v12_1_live_paper_contract.py",
    "build_v12_1_live_paper_run_registry.py",
    "build_v12_1_live_paper_due_schedule.py",
    "update_v12_1_live_paper_status.py",
    "build_v12_1_live_paper_delta_report.py",
    "audit_v12_1_live_paper_loop.py",
    "build_v12_1_live_paper_closeout.py",
]


def main():
    ok = True
    for s in STEPS:
        r = subprocess.run(
            ["python3", str(W / "scripts/cases" / s)],
            cwd=str(W),
            capture_output=True,
            text=True,
        )
        status = "OK" if r.returncode == 0 else "FAIL"
        print(f"{status}: {s} {r.stdout.strip()[:120]}")
        if r.returncode != 0:
            print(f"  stderr: {r.stderr.strip()[:200]}")
            ok = False

    # Read final states
    co = json.loads((C / "v12_1_live_paper_closeout.json").read_text()) if (C / "v12_1_live_paper_closeout.json").exists() else {}
    audit = json.loads((C / "v12_1_live_paper_loop_audit.json").read_text()) if (C / "v12_1_live_paper_loop_audit.json").exists() else {}
    v12_co = json.loads((C / "v12_research_only_closeout.json").read_text()) if (C / "v12_research_only_closeout.json").exists() else {}

    v12_confirmed = "CONFIRMED" in v12_co.get("status", "")
    lp_confirmed = "CONFIRMED" in co.get("status", "")
    audit_pass = "PASS" in audit.get("status", "")

    final_ok = ok and v12_confirmed and lp_confirmed and audit_pass

    result = {
        "status": "V12_1_LIVE_PAPER_FULL_CHAIN_PASS" if final_ok else "V12_1_LIVE_PAPER_FULL_CHAIN_BLOCKED",
        "steps": STEPS,
        "steps_returncode_pass": ok,
        "v12_research_only_base_confirmed": v12_confirmed,
        "live_paper_loop_confirmed": lp_confirmed,
        "live_paper_completion_status": co.get("live_paper_completion_status", "UNKNOWN"),
        "closeout_status": co.get("status", "UNKNOWN"),
        "audit_status": audit.get("status", "UNKNOWN"),
        "forbidden_action_violations": audit.get("forbidden_action_violations", []),
        "rejected_reactivation_violations": audit.get("rejected_reactivation_violations", []),
        "next_required_action": co.get("next_required_action", "UNKNOWN"),
        "ready_for_alpha_claim": False,
        "alpha_validated": False,
        "production": "BLOCKED",
        "broker_runtime": "BLOCKED",
        "real_trade": "BLOCKED",
    }

    json.dump(result, open(C / "v12_1_live_paper_full_chain.json", "w"), indent=2)
    print(f"\nV12.1 Full Chain: {result['status']} | completion={result['live_paper_completion_status']}")


if __name__ == "__main__":
    main()
