#!/usr/bin/env python3
"""Build V12 Entry Gate Recheck Report."""
import json
from pathlib import Path
W = Path(__file__).resolve().parent.parent.parent
C = W / "runtime_reports" / "cases"
g = json.loads((C / "v12_alpha_operating_loop_entry_gate.json").read_text())
v6 = json.loads((C / "v11_6_closeout.json").read_text())
next_action = "COMPLETE_OOS_PAPER_TRACKING_PERIOD" if not v6.get("paper_tracking_period_completed", True) else "ALL_GATES_PASS_READY_FOR_V12"
r = {
    "status": "V12_ENTRY_GATE_RECHECK_BUILT",
    "v12_gate_status": g["status"],
    "blocking_reasons": g.get("blocking_reasons", []),
    "next_required_action": next_action,
    "ready_for_alpha_claim": False,
    "alpha_validated": False,
    "production": "BLOCKED",
    "broker_runtime": "BLOCKED",
    "real_trade": "BLOCKED",
}
json.dump(r, open(C / "v12_entry_gate_recheck_report.json", "w"), indent=2)
print(f"Recheck: {g['status']} next={next_action}")
