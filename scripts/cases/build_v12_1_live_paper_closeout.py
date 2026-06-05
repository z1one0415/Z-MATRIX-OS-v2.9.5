#!/usr/bin/env python3
"""V12.1: Live Paper Closeout — aggregate all V12.1 outputs and determine next action."""
import json
from pathlib import Path

W = Path(__file__).resolve().parent.parent.parent
C = W / "runtime_reports" / "cases"


def load(name: str) -> dict:
    p = C / name
    return json.loads(p.read_text()) if p.exists() else {}


def main():
    contract = load("v12_1_live_paper_contract.json")
    registry = load("v12_1_live_paper_run_registry.json")
    schedule = load("v12_1_live_paper_due_schedule.json")
    status_update = load("v12_1_live_paper_status_update.json")
    delta = load("v12_1_live_paper_delta_report.json")
    audit = load("v12_1_live_paper_loop_audit.json")

    contract_built = "BUILT" in contract.get("status", "")
    registry_built = "BUILT" in registry.get("status", "")
    schedule_built = "BUILT" in schedule.get("status", "")
    status_built = "BUILT" in status_update.get("status", "")
    delta_built = "BUILT" in delta.get("status", "")
    audit_pass = "PASS" in audit.get("status", "")

    all_components_ok = all([contract_built, registry_built, schedule_built, status_built, delta_built, audit_pass])

    # Safety verification
    safety_ok = all([
        contract.get("ready_for_alpha_claim", True) is False,
        contract.get("alpha_validated", True) is False,
        contract.get("production") == "BLOCKED",
        contract.get("broker_runtime") == "BLOCKED",
        contract.get("real_trade") == "BLOCKED",
    ])

    no_actions = all([
        registry.get("investment_action_count", -1) == 0,
        registry.get("trade_action_count", -1) == 0,
        schedule.get("investment_action_count", 0) == 0,
        schedule.get("trade_action_count", 0) == 0,
        status_update.get("investment_action_count", 0) == 0,
        status_update.get("trade_action_count", 0) == 0,
        delta.get("investment_action_count", -1) == 0,
        delta.get("trade_action_count", -1) == 0,
    ])

    # Check for rejected reactivation
    rejected_count = registry.get("rejected_preserved_count", 0)
    schedule_scheduled = schedule.get("scheduled_run_count", 0)
    active_in_registry = registry.get("active_live_paper_run_count", 0)
    rejected_ok = schedule_scheduled == active_in_registry  # schedule should only contain active

    completion_status = status_update.get("live_paper_completion_status", "UNKNOWN")
    all_completed = status_update.get("all_live_paper_runs_completed", False)

    # Determine next action
    if all_completed:
        next_action = "V12_2_RESEARCH_ONLY_Z9_FEEDBACK_LOOP"
    else:
        next_action = "WAIT_FOR_LIVE_PAPER_DUE_LABELS"

    closeout_passed = all_components_ok and safety_ok and no_actions and rejected_ok

    result = {
        "status": "V12_1_LIVE_PAPER_LOOP_CONFIRMED" if closeout_passed else "V12_1_LIVE_PAPER_LOOP_INCOMPLETE",
        "live_paper_loop_confirmed": closeout_passed,
        "live_paper_completion_status": completion_status,
        "components": {
            "contract_built": contract_built,
            "registry_built": registry_built,
            "schedule_built": schedule_built,
            "status_update_built": status_built,
            "delta_report_built": delta_built,
            "audit_pass": audit_pass,
        },
        "safety_blocked": safety_ok,
        "no_trading_actions": no_actions,
        "rejected_not_reactivated": rejected_ok,
        "active_run_count": active_in_registry,
        "rejected_preserved_count": rejected_count,
        "next_required_action": next_action,
        "ready_for_alpha_claim": False,
        "alpha_validated": False,
        "production": "BLOCKED",
        "broker_runtime": "BLOCKED",
        "real_trade": "BLOCKED",
    }

    json.dump(result, open(C / "v12_1_live_paper_closeout.json", "w"), indent=2)
    print(f"V12.1 Closeout: {result['status']} | completion={completion_status} | next={next_action}")


if __name__ == "__main__":
    main()
