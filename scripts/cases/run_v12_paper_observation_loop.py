#!/usr/bin/env python3
"""V12.0: Paper Observation Loop — establish next-round paper tracking for each research signal."""
import json
from pathlib import Path

W = Path(__file__).resolve().parent.parent.parent
C = W / "runtime_reports" / "cases"


def load(name: str) -> dict:
    p = C / name
    return json.loads(p.read_text()) if p.exists() else {}


def main():
    snapshot = load("v12_research_signal_snapshot.json")
    contract = load("v12_research_only_operating_contract.json")

    research_only = contract.get("research_only", False)

    observations = []
    for sig in snapshot.get("signals", []):
        fid = sig.get("factor_id", "UNKNOWN")
        horizon = sig.get("horizon", "UNKNOWN")
        state = sig.get("research_signal_state", "REJECT")

        # Rejected signals get TRACKING_REJECTED
        obs_status = "PAPER_TRACKING_PENDING" if state != "REJECT" else "TRACKING_REJECTED"

        obs = {
            "paper_observation_id": f"V12_PO_{len(observations)+1:03d}",
            "research_signal_id": sig.get("research_signal_id", ""),
            "factor_id": fid,
            "horizon": horizon,
            "start_as_of_date": "20240905",
            "tracking_horizon": horizon,
            "status": obs_status,
            "paper_only": True,
            "investment_action": "NONE",
            "trade_action": "NONE",
        }
        observations.append(obs)

    pending_count = sum(1 for o in observations if o["status"] == "PAPER_TRACKING_PENDING")

    result = {
        "status": "V12_PAPER_OBSERVATION_LOOP_BUILT",
        "observation_count": len(observations),
        "pending_observation_count": pending_count,
        "rejected_observation_count": len(observations) - pending_count,
        "observations": observations,
        "paper_only": True,
        "investment_action_count": 0,
        "trade_action_count": 0,
        "ready_for_alpha_claim": False,
        "alpha_validated": False,
        "production": "BLOCKED",
        "broker_runtime": "BLOCKED",
        "real_trade": "BLOCKED",
    }

    json.dump(result, open(C / "v12_paper_observation_loop.json", "w"), indent=2)
    print(f"V12.0 Paper Observation Loop: {len(observations)} observations | pending={pending_count}")


if __name__ == "__main__":
    main()
