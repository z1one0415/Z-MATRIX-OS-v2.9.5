#!/usr/bin/env python3
"""V12.1: Live Paper Due Schedule — establish future-label requirements for each active run."""
import json
from pathlib import Path

W = Path(__file__).resolve().parent.parent.parent
C = W / "runtime_reports" / "cases"


def load(name: str) -> dict:
    p = C / name
    return json.loads(p.read_text()) if p.exists() else {}


def main():
    registry = load("v12_1_live_paper_run_registry.json")
    contract = load("v12_1_live_paper_contract.json")

    schedule_items = []
    for run in registry.get("runs", []):
        if run.get("run_status") == "LIVE_PAPER_PENDING":
            horizon = run.get("horizon", "T20")
            item = {
                "live_paper_run_id": run["live_paper_run_id"],
                "research_signal_id": run.get("research_signal_id", ""),
                "factor_id": run.get("factor_id", ""),
                "horizon": horizon,
                "schedule_status": "WAITING_FOR_FUTURE_LABEL",
                "required_label_horizon": horizon,
                "required_label_status": "NOT_YET_AVAILABLE",
                "paper_only": True,
                "investment_action": "NONE",
                "trade_action": "NONE",
            }
            schedule_items.append(item)

    # Fail-closed: initially all are WAITING_FOR_FUTURE_LABEL
    ready_for_completion = False

    result = {
        "status": "V12_1_LIVE_PAPER_DUE_SCHEDULE_BUILT",
        "scheduled_run_count": len(schedule_items),
        "waiting_for_future_label_count": len(schedule_items),
        "ready_for_completion": ready_for_completion,
        "schedule_items": schedule_items,
        "blocking_reasons": ["LIVE_PAPER_FUTURE_LABELS_NOT_AVAILABLE"] if not ready_for_completion else [],
        "ready_for_alpha_claim": False,
        "alpha_validated": False,
        "production": "BLOCKED",
        "broker_runtime": "BLOCKED",
        "real_trade": "BLOCKED",
    }

    json.dump(result, open(C / "v12_1_live_paper_due_schedule.json", "w"), indent=2)
    print(f"V12.1 Due Schedule: {len(schedule_items)} scheduled | waiting={len(schedule_items)}")


if __name__ == "__main__":
    main()
