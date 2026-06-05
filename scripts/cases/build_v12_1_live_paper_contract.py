#!/usr/bin/env python3
"""V12.1: Build Live Paper Contract — scope lock for rolling live-paper research loop."""
import json
from pathlib import Path

W = Path(__file__).resolve().parent.parent.parent
C = W / "runtime_reports" / "cases"


def load(name: str) -> dict:
    p = C / name
    return json.loads(p.read_text()) if p.exists() else {}


def main():
    closeout = load("v12_research_only_closeout.json")
    contract = load("v12_research_only_operating_contract.json")
    snapshot = load("v12_research_signal_snapshot.json")
    obs_loop = load("v12_paper_observation_loop.json")

    v12_confirmed = "CONFIRMED" in closeout.get("status", "")
    research_only = contract.get("research_only", False)

    pending_count = obs_loop.get("pending_observation_count", 0)
    obs_total = obs_loop.get("observation_count", 0)
    rejected_count = obs_total - pending_count

    ct = {
        "status": (
            "V12_1_LIVE_PAPER_CONTRACT_BUILT"
            if (v12_confirmed and research_only)
            else "V12_1_LIVE_PAPER_CONTRACT_BLOCKED"
        ),
        "source_v12_closeout": closeout.get("status", "UNKNOWN"),
        "operating_mode": "RESEARCH_ONLY_LIVE_PAPER_LOOP" if (v12_confirmed and research_only) else "BLOCKED",
        "research_only": research_only,
        "source_signal_count": snapshot.get("research_signal_count", 0),
        "pending_observation_count": pending_count,
        "rejected_observation_count": rejected_count,
        "activation_policy": "PENDING_ONLY",
        "rejected_policy": "KEEP_REJECTED",
        "tracking_horizons": ["T20", "T60"],
        "fail_closed": True,
        "ready_for_alpha_claim": False,
        "alpha_validated": False,
        "production": "BLOCKED",
        "broker_runtime": "BLOCKED",
        "real_trade": "BLOCKED",
    }

    json.dump(ct, open(C / "v12_1_live_paper_contract.json", "w"), indent=2)
    print(f"V12.1 Contract: {ct['status']} | pending={pending_count} rejected={rejected_count}")


if __name__ == "__main__":
    main()
