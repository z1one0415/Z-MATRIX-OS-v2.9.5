#!/usr/bin/env python3
"""V12 Gate — reads ALL V11.5-V11.9 closeouts, strict fail-closed."""
import json
from pathlib import Path

W = Path(__file__).resolve().parent.parent.parent
C = W / "runtime_reports" / "cases"

def load(name):
    p = C / name
    return json.loads(p.read_text()) if p.exists() else {}

def main():
    v5 = load("v11_5_full_reproducible_chain.json")
    v5_ok = v5.get("status") == "V11_5_FULL_REPRODUCIBLE_CHAIN_PASS"
    v6 = load("v11_6_closeout.json")
    v6_ok = v6.get("status") == "V11_6_OOS_PAPER_TRACKING_FRAMEWORK_CONFIRMED"
    v6_track_ok = v6.get("paper_tracking_period_completed", False)
    v7 = load("v11_7_closeout.json")
    v7_ok = v7.get("status") == "V11_7_COST_MODEL_UPGRADE_CONFIRMED"
    v7_cost_ok = v7.get("cost_model_status", "PROXY_ONLY") != "PROXY_ONLY"
    v8 = load("v11_8_closeout.json")
    v8_ok = v8.get("substage_confirmed", False)
    v8_oos = v8.get("valid_oos_count", 0) >= v8.get("minimum_oos_period_required", 2)
    v9 = load("v11_9_closeout.json")
    v9_ok = v9.get("substage_confirmed", False)
    v9_autopsy = v9.get("autopsy_input_ready", False)

    reasons = []
    if not v5_ok: reasons.append("V11_5_NOT_CONFIRMED")
    if not v6_ok: reasons.append("V11_6_NOT_CONFIRMED")
    if not v6_track_ok: reasons.append("PAPER_TRACKING_PERIOD_NOT_COMPLETED")
    if not v7_ok: reasons.append("V11_7_NOT_CONFIRMED")
    if not v7_cost_ok: reasons.append("COST_MODEL_PROXY_ONLY")
    if not v8_ok: reasons.append("V11_8_NOT_CONFIRMED")
    if not v8_oos: reasons.append("INSUFFICIENT_WALK_FORWARD_PERIODS")
    if not v9_ok: reasons.append("V11_9_NOT_CONFIRMED")
    if not v9_autopsy: reasons.append("Z9_AUTOPSY_INPUT_NOT_READY")

    blocked = len(reasons) > 0
    g = {
        "status": "V12_ALPHA_OPERATING_LOOP_ENTRY_BLOCKED" if blocked else "V12_ALPHA_OPERATING_LOOP_RESEARCH_ONLY_ALLOWED",
        "ready_for_alpha_operating_loop": not blocked,
        "research_only": True,
        "blocking_reasons": reasons,
        "ready_for_alpha_claim": False,
        "alpha_validated": False,
        "production": "BLOCKED",
        "broker_runtime": "BLOCKED",
        "real_trade": "BLOCKED",
    }
    json.dump(g, open(C / "v12_alpha_operating_loop_entry_gate.json", "w"), indent=2)
    print(f"V12 Gate: {g['status']} | reasons={reasons}")

if __name__ == "__main__":
    main()
