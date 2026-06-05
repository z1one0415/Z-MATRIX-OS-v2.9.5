#!/usr/bin/env python3
"""V12.1: Live Paper Delta Report — status change summary for rolling live-paper tracking."""
import json
from pathlib import Path

W = Path(__file__).resolve().parent.parent.parent
C = W / "runtime_reports" / "cases"


def load(name: str) -> dict:
    p = C / name
    return json.loads(p.read_text()) if p.exists() else {}


def main():
    registry = load("v12_1_live_paper_run_registry.json")
    status_update = load("v12_1_live_paper_status_update.json")
    snapshot = load("v12_research_signal_snapshot.json")

    # Build baseline counts from registry (before update)
    orig_active = registry.get("active_live_paper_run_count", 0)
    orig_rejected = registry.get("rejected_preserved_count", 0)

    # Current counts from status update
    completed = status_update.get("completed_run_count", 0)
    waiting = status_update.get("waiting_run_count", 0)
    blocked = status_update.get("blocked_run_count", 0)

    # Delta: new completed = completed (from status update) minus ... 
    # Initially all were "LIVE_PAPER_PENDING" → none were completed
    # New completed = completed from status update
    # New waiting = waiting (statuses that moved to WAITING_FOR_LABEL)
    # New blocked = preserved rejected
    new_completed = completed
    new_waiting = waiting
    new_blocked = blocked

    result = {
        "status": "V12_1_LIVE_PAPER_DELTA_REPORT_BUILT",
        "active_run_count": orig_active,
        "completed_run_count": completed,
        "waiting_run_count": waiting,
        "blocked_run_count": blocked,
        "delta_summary": {
            "new_completed": new_completed,
            "new_waiting": new_waiting,
            "new_blocked": new_blocked,
        },
        "research_only": True,
        "paper_only": True,
        "investment_action_count": 0,
        "trade_action_count": 0,
        "ready_for_alpha_claim": False,
        "alpha_validated": False,
        "production": "BLOCKED",
        "broker_runtime": "BLOCKED",
        "real_trade": "BLOCKED",
    }

    json.dump(result, open(C / "v12_1_live_paper_delta_report.json", "w"), indent=2)
    print(f"V12.1 Delta: completed={completed} waiting={waiting} blocked={blocked}")


if __name__ == "__main__":
    main()
