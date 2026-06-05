#!/usr/bin/env python3
"""V12.0: Research-Only Full Chain Runner — orchestrates V12 gate→contract→signal→obs→autopsy→audit→closeout."""
import subprocess
import json
from pathlib import Path

W = Path(__file__).resolve().parent.parent.parent
C = W / "runtime_reports" / "cases"

STEPS = [
    "check_v12_alpha_operating_loop_entry_gate.py",
    "build_v12_research_only_operating_contract.py",
    "build_v12_research_signal_snapshot.py",
    "run_v12_paper_observation_loop.py",
    "write_v12_z9_research_autopsy_input.py",
    "audit_v12_research_only_loop.py",
    "build_v12_research_only_closeout.py",
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
        print(f"{status}: {s} {r.stdout.strip()[:100]}")
        if r.returncode != 0:
            print(f"  stderr: {r.stderr.strip()[:200]}")
            ok = False

    # Read final states
    co = json.loads((C / "v12_research_only_closeout.json").read_text()) if (C / "v12_research_only_closeout.json").exists() else {}
    audit = json.loads((C / "v12_research_only_loop_audit.json").read_text()) if (C / "v12_research_only_loop_audit.json").exists() else {}
    gate = json.loads((C / "v12_alpha_operating_loop_entry_gate.json").read_text()) if (C / "v12_alpha_operating_loop_entry_gate.json").exists() else {}

    final_ok = (
        ok
        and "CONFIRMED" in co.get("status", "")
        and "PASS" in audit.get("status", "")
    )

    result = {
        "status": "V12_RESEARCH_ONLY_FULL_CHAIN_PASS" if final_ok else "V12_RESEARCH_ONLY_FULL_CHAIN_BLOCKED",
        "steps": STEPS,
        "steps_returncode_pass": ok,
        "v12_gate_status": gate.get("status", "UNKNOWN"),
        "research_only_loop_confirmed": "CONFIRMED" in co.get("status", ""),
        "closeout_status": co.get("status", "UNKNOWN"),
        "audit_status": audit.get("status", "UNKNOWN"),
        "forbidden_action_violations": audit.get("forbidden_action_violations", []),
        "ready_for_alpha_claim": False,
        "alpha_validated": False,
        "production": "BLOCKED",
        "broker_runtime": "BLOCKED",
        "real_trade": "BLOCKED",
    }

    json.dump(result, open(C / "v12_research_only_full_chain.json", "w"), indent=2)
    print(f"\nV12.0 Full Chain: {result['status']} | steps_ok={ok} | closeout={result['closeout_status']}")


if __name__ == "__main__":
    main()
