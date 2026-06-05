#!/usr/bin/env python3
"""V12.0: Z9 Research Autopsy Input Writer — prepare factor-level autopsy data from research signals."""
import json
from pathlib import Path

W = Path(__file__).resolve().parent.parent.parent
C = W / "runtime_reports" / "cases"


def load(name: str) -> dict:
    p = C / name
    return json.loads(p.read_text()) if p.exists() else {}


def main():
    snapshot = load("v12_research_signal_snapshot.json")
    obs_loop = load("v12_paper_observation_loop.json")
    oos_outcomes = load("v11_6_1_oos_paper_outcomes.json")

    # Build hit/miss by factor+horizon from OOS outcomes
    hit_map = {}
    for obs in oos_outcomes.get("observations", []):
        fid = obs.get("factor_id", "")
        horizon = obs.get("horizon", "")
        key = f"{fid}|{horizon}"
        if key not in hit_map:
            hit_map[key] = {"hits": 0, "misses": 0}
        if obs.get("direction_hit", False):
            hit_map[key]["hits"] += 1
        else:
            hit_map[key]["misses"] += 1

    autopsy_inputs = []
    for sig in snapshot.get("signals", []):
        fid = sig.get("factor_id", "UNKNOWN")
        horizon = sig.get("horizon", "UNKNOWN")
        key = f"{fid}|{horizon}"
        hit_data = hit_map.get(key, {"hits": 0, "misses": 0})
        total = hit_data["hits"] + hit_data["misses"]
        hit_rate = hit_data["hits"] / total if total > 0 else 0.0

        inp = {
            "z9_input_id": f"V12_Z9I_{len(autopsy_inputs)+1:03d}",
            "factor_id": fid,
            "research_signal_id": sig.get("research_signal_id", ""),
            "oos_hit_rate": round(hit_rate, 4),
            "direction_hit_count": hit_data["hits"],
            "direction_miss_count": hit_data["misses"],
            "cost_sensitivity": sig.get("cost_adjusted_status", "UNKNOWN"),
            "walk_forward_support": sig.get("walk_forward_status", "UNKNOWN"),
            "lifecycle_candidate_state": sig.get("z9_lifecycle_state", "KEEP_OBSERVING"),
            "diagnosis_scope": "RESEARCH_ONLY",
            "paper_only": True,
            "investment_action": "NONE",
            "trade_action": "NONE",
        }
        autopsy_inputs.append(inp)

    result = {
        "status": "V12_Z9_RESEARCH_AUTOPSY_INPUT_BUILT",
        "input_count": len(autopsy_inputs),
        "autopsy_inputs": autopsy_inputs,
        "paper_only": True,
        "investment_action_count": 0,
        "trade_action_count": 0,
        "ready_for_alpha_claim": False,
        "alpha_validated": False,
        "production": "BLOCKED",
        "broker_runtime": "BLOCKED",
        "real_trade": "BLOCKED",
    }

    json.dump(result, open(C / "v12_z9_research_autopsy_input.json", "w"), indent=2)
    print(f"V12.0 Z9 Autopsy Input: {len(autopsy_inputs)} inputs")


if __name__ == "__main__":
    main()
