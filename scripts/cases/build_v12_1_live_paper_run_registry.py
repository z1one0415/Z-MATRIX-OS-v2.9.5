#!/usr/bin/env python3
"""V12.1: Live Paper Run Registry — activate PENDING observations, preserve REJECTED."""
import json
from pathlib import Path

W = Path(__file__).resolve().parent.parent.parent
C = W / "runtime_reports" / "cases"


def load(name: str) -> dict:
    p = C / name
    return json.loads(p.read_text()) if p.exists() else {}


def main():
    contract = load("v12_1_live_paper_contract.json")
    obs_loop = load("v12_paper_observation_loop.json")
    snapshot = load("v12_research_signal_snapshot.json")

    # Build signal lookup
    signal_map = {}
    for sig in snapshot.get("signals", []):
        signal_map[sig["research_signal_id"]] = sig

    runs = []
    rejected_count = 0
    for obs in obs_loop.get("observations", []):
        obs_status = obs.get("status", "UNKNOWN")
        rs_id = obs.get("research_signal_id", "")
        sig = signal_map.get(rs_id, {})

        if obs_status == "PAPER_TRACKING_PENDING":
            run_status = "LIVE_PAPER_PENDING"
        elif obs_status == "TRACKING_REJECTED":
            run_status = "PRESERVED_REJECTED"
            rejected_count += 1
        else:
            run_status = "UNKNOWN_STATUS"

        run = {
            "live_paper_run_id": f"V12_1_LPR_{len(runs)+1:03d}",
            "source_paper_observation_id": obs.get("paper_observation_id", ""),
            "research_signal_id": rs_id,
            "factor_id": obs.get("factor_id", ""),
            "horizon": obs.get("horizon", ""),
            "source_signal_state": sig.get("research_signal_state", "UNKNOWN"),
            "run_status": run_status,
            "paper_only": True,
            "investment_action": "NONE",
            "trade_action": "NONE",
        }
        runs.append(run)

    active_count = sum(1 for r in runs if r["run_status"] == "LIVE_PAPER_PENDING")
    rejected_preserved = sum(1 for r in runs if r["run_status"] == "PRESERVED_REJECTED")

    result = {
        "status": "V12_1_LIVE_PAPER_RUN_REGISTRY_BUILT",
        "source_observation_count": len(runs),
        "active_live_paper_run_count": active_count,
        "rejected_preserved_count": rejected_preserved,
        "runs": runs,
        "investment_action_count": 0,
        "trade_action_count": 0,
        "ready_for_alpha_claim": False,
        "alpha_validated": False,
        "production": "BLOCKED",
        "broker_runtime": "BLOCKED",
        "real_trade": "BLOCKED",
    }

    json.dump(result, open(C / "v12_1_live_paper_run_registry.json", "w"), indent=2)
    print(f"V12.1 Registry: {len(runs)} total | active={active_count} rejected_preserved={rejected_preserved}")


if __name__ == "__main__":
    main()
