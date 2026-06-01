#!/usr/bin/env python3
"""V9-E: V10 Council Research Entry Gate — reads all V9 evidence."""
import json
from pathlib import Path

W = Path(__file__).resolve().parent.parent.parent
CASES = W / "runtime_reports" / "cases"


def load(name):
    p = CASES / name
    return json.loads(p.read_text()) if p.exists() else {}


def main():
    stability = load("v9_formal_factor_stability.json")
    decay_data = load("v9_factor_decay_analysis.json")
    robustness = load("v9_factor_robustness.json")
    selection = load("v9_factor_selection_gate.json")
    closeout = load("case_expansion_v9_closeout.json")

    blocking = []

    if stability.get("status") != "V9_FORMAL_FACTOR_STABILITY_BUILT":
        blocking.append("STABILITY_NOT_BUILT")
    if decay_data.get("status") != "V9_FACTOR_DECAY_ANALYSIS_BUILT":
        blocking.append("DECAY_NOT_BUILT")
    if robustness.get("status") != "V9_FACTOR_ROBUSTNESS_BUILT":
        blocking.append("ROBUSTNESS_NOT_BUILT")
    if selection.get("status") != "V9_FACTOR_SELECTION_GATE_BUILT":
        blocking.append("SELECTION_GATE_NOT_BUILT")

    promoted = selection.get("promoted_factor_count", 0)
    if promoted < 1:
        blocking.append("NO_PROMOTED_FACTORS")

    if (
        stability.get("ready_for_alpha_claim", True)
        or decay_data.get("alpha_validated", True)
        or robustness.get("alpha_validated", True)
        or selection.get("alpha_validated", True)
    ):
        blocking.append("ALPHA_CLAIM_DETECTED")

    if (
        closeout.get("production", "") != "BLOCKED"
        or closeout.get("broker_runtime", "") != "BLOCKED"
        or closeout.get("real_trade", "") != "BLOCKED"
    ):
        blocking.append("SAFETY_NOT_BLOCKED")

    allowed = len(blocking) == 0

    gate = {
        "status": (
            "V10_COUNCIL_RESEARCH_ENTRY_ALLOWED"
            if allowed
            else "V10_COUNCIL_RESEARCH_ENTRY_BLOCKED"
        ),
        "ready_for_council_research_review": allowed,
        "promoted_factor_count": promoted,
        "watch_factor_count": selection.get("watch_factor_count", 0),
        "ready_for_alpha_claim": False,
        "alpha_validated": False,
        "blocking_reasons": blocking,
        "production": "BLOCKED",
        "broker_runtime": "BLOCKED",
        "real_trade": "BLOCKED",
    }
    (CASES / "v10_council_research_entry_gate.json").write_text(
        json.dumps(gate, indent=2, ensure_ascii=False)
    )
    print(
        f"V10 Gate: {'ALLOWED' if allowed else 'BLOCKED'} "
        f"| promoted={promoted} | blocking={blocking}"
    )


if __name__ == "__main__":
    main()
