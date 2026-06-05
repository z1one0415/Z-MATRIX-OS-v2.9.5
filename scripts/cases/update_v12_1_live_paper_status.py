#!/usr/bin/env python3
"""V12.1: Live Paper Status Updater — check forward label availability from v8_forward_return_labels."""
import json
from pathlib import Path

W = Path(__file__).resolve().parent.parent.parent
C = W / "runtime_reports" / "cases"


def load(name: str) -> dict:
    p = C / name
    return json.loads(p.read_text()) if p.exists() else {}


def load_forward_labels() -> dict:
    """Load v8 forward labels and index by (as_of_date, horizon) → count of available labels."""
    p = C / "v8_large_data" / "v8_forward_return_labels.json"
    if not p.exists():
        return {}
    data = json.loads(p.read_text())
    # Build a lookup: (as_of_date, horizon) → available label count
    index = {}
    for lbl in data.get("labels", []):
        key = (lbl.get("as_of_date", ""), lbl.get("horizon", ""))
        if key not in index:
            index[key] = {"count": 0, "sample_ticker": lbl.get("ticker", "")}
        index[key]["count"] += 1
        if lbl.get("future_relative_return", 0) != 0 or lbl.get("future_stock_return", 0) != 0:
            if "has_real_returns" not in index[key]:
                index[key]["has_real_returns"] = True
    return index


def main():
    registry = load("v12_1_live_paper_run_registry.json")
    due_schedule = load("v12_1_live_paper_due_schedule.json")
    forward_labels = load_forward_labels()

    base_date = "20240905"
    updated_runs = []
    completed = 0
    waiting = 0
    blocked = 0

    for run in registry.get("runs", []):
        run_id = run.get("live_paper_run_id", "")
        horizon = run.get("horizon", "T20")
        orig_status = run.get("run_status", "")

        if orig_status == "PRESERVED_REJECTED":
            # Keep rejected
            updated_runs.append({**run, "run_status": "PRESERVED_REJECTED"})
            blocked += 1
            continue

        # Check forward label availability
        label_key = (base_date, horizon)
        label_info = forward_labels.get(label_key, {})

        if label_info.get("count", 0) > 0:
            new_status = "COMPLETED"
            completed += 1
        else:
            new_status = "WAITING_FOR_LABEL"
            waiting += 1

        updated_runs.append({
            **run,
            "run_status": new_status,
            "forward_labels_available": label_info.get("count", 0),
            "forward_label_base_date": base_date,
        })

    all_completed = completed == len(updated_runs) - blocked
    completion_status = (
        "COMPLETED" if all_completed
        else "PARTIAL_COMPLETION" if completed > 0
        else "WAITING_FOR_LABELS"
    )

    result = {
        "status": "V12_1_LIVE_PAPER_STATUS_UPDATE_BUILT",
        "active_run_count": len([r for r in updated_runs if r.get("run_status") == "COMPLETED" or r.get("run_status") == "WAITING_FOR_LABEL"]),
        "completed_run_count": completed,
        "waiting_run_count": waiting,
        "blocked_run_count": blocked,
        "all_live_paper_runs_completed": all_completed,
        "live_paper_completion_status": completion_status,
        "updated_runs": updated_runs,
        "blocking_reasons": ["LIVE_PAPER_FUTURE_LABELS_NOT_AVAILABLE"] if not all_completed else [],
        "ready_for_alpha_claim": False,
        "alpha_validated": False,
        "production": "BLOCKED",
        "broker_runtime": "BLOCKED",
        "real_trade": "BLOCKED",
    }

    json.dump(result, open(C / "v12_1_live_paper_status_update.json", "w"), indent=2)
    print(f"V12.1 Status: {completion_status} | completed={completed} waiting={waiting} blocked={blocked}")


if __name__ == "__main__":
    main()
