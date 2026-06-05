#!/usr/bin/env python3
"""V12.0: Research-Only Closeout — aggregate all V12 outputs and confirm loop integrity."""
import json
from pathlib import Path

W = Path(__file__).resolve().parent.parent.parent
C = W / "runtime_reports" / "cases"


def load(name: str) -> dict:
    p = C / name
    return json.loads(p.read_text()) if p.exists() else {}


def main():
    contract = load("v12_research_only_operating_contract.json")
    snapshot = load("v12_research_signal_snapshot.json")
    obs_loop = load("v12_paper_observation_loop.json")
    autopsy = load("v12_z9_research_autopsy_input.json")
    audit = load("v12_research_only_loop_audit.json")

    contract_built = "BUILT" in contract.get("status", "")
    snapshot_built = "BUILT" in snapshot.get("status", "")
    obs_built = "BUILT" in obs_loop.get("status", "")
    autopsy_built = "BUILT" in autopsy.get("status", "")
    audit_pass = "PASS" in audit.get("status", "")

    all_components_ok = all([contract_built, snapshot_built, obs_built, autopsy_built, audit_pass])

    # Safety verification
    safety_ok = all([
        contract.get("ready_for_alpha_claim", True) is False,
        contract.get("alpha_validated", True) is False,
        contract.get("production") == "BLOCKED",
        contract.get("broker_runtime") == "BLOCKED",
        contract.get("real_trade") == "BLOCKED",
    ])

    no_actions = all([
        snapshot.get("investment_action_count", -1) == 0,
        snapshot.get("trade_action_count", -1) == 0,
        obs_loop.get("investment_action_count", -1) == 0,
        obs_loop.get("trade_action_count", -1) == 0,
        autopsy.get("investment_action_count", -1) == 0,
        autopsy.get("trade_action_count", -1) == 0,
    ])

    closeout_passed = all_components_ok and safety_ok and no_actions

    result = {
        "status": "V12_RESEARCH_ONLY_OPERATING_LOOP_CONFIRMED" if closeout_passed else "V12_RESEARCH_ONLY_OPERATING_LOOP_INCOMPLETE",
        "research_only_loop_confirmed": closeout_passed,
        "components": {
            "contract_built": contract_built,
            "signal_snapshot_built": snapshot_built,
            "paper_observation_loop_built": obs_built,
            "z9_autopsy_input_built": autopsy_built,
            "audit_pass": audit_pass,
        },
        "safety_blocked": safety_ok,
        "no_trading_actions": no_actions,
        "contract_status": contract.get("status", "UNKNOWN"),
        "snapshot_status": snapshot.get("status", "UNKNOWN"),
        "obs_loop_status": obs_loop.get("status", "UNKNOWN"),
        "autopsy_status": autopsy.get("status", "UNKNOWN"),
        "audit_status": audit.get("status", "UNKNOWN"),
        "ready_for_alpha_claim": False,
        "alpha_validated": False,
        "production": "BLOCKED",
        "broker_runtime": "BLOCKED",
        "real_trade": "BLOCKED",
        "next_required_action": "V12_1_RESEARCH_ONLY_LIVE_PAPER_LOOP_EXTENSION",
    }

    json.dump(result, open(C / "v12_research_only_closeout.json", "w"), indent=2)
    print(f"V12.0 Closeout: {result['status']} | "
          f"components={'OK' if all_components_ok else 'FAIL'} "
          f"safety={'OK' if safety_ok else 'FAIL'} "
          f"no_actions={'OK' if no_actions else 'FAIL'}")


if __name__ == "__main__":
    main()
