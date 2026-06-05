#!/usr/bin/env python3
"""V12.1: Live Paper Status Updater — validate per-run required_label_key against v8_forward_return_labels."""
import json
from pathlib import Path

W = Path(__file__).resolve().parent.parent.parent
C = W / "runtime_reports" / "cases"


def load(name: str) -> dict:
    p = C / name
    return json.loads(p.read_text()) if p.exists() else {}


def load_forward_label_index() -> dict:
    """Index v8 forward labels by (as_of_date, horizon) with count."""
    p = C / "v8_large_data" / "v8_forward_return_labels.json"
    if not p.exists():
        return {}
    data = json.loads(p.read_text())
    index = {}
    for lbl in data.get("labels", []):
        key = (lbl.get("as_of_date", ""), lbl.get("horizon", ""))
        if key not in index:
            index[key] = 0
        index[key] += 1
    return index


def main():
    registry = load("v12_1_live_paper_run_registry.json")
    due_schedule = load("v12_1_live_paper_due_schedule.json")
    forward_labels = load_forward_label_index()

    blocking_reasons = []
    completed = 0
    waiting = 0
    blocked = 0
    reused_date_count = 0

    # Build schedule lookup by live_paper_run_id
    schedule_map = {}
    for item in due_schedule.get("schedule_items", []):
        schedule_map[item.get("live_paper_run_id", "")] = item

    updated_runs = []
    for run in registry.get("runs", []):
        run_id = run.get("live_paper_run_id", "")
        orig_status = run.get("run_status", "")

        if orig_status == "PRESERVED_REJECTED":
            updated_runs.append({
                **run,
                "run_status": "PRESERVED_REJECTED",
                "label_source": "",
                "label_key_validated": False,
            })
            blocked += 1
            continue

        schedule_item = schedule_map.get(run_id, {})
        required_key = schedule_item.get("required_label_key", {})
        req_date = required_key.get("as_of_date", "")
        req_horizon = required_key.get("horizon", "")
        source_date = schedule_item.get("source_start_as_of_date", "")

        # Hardgate: check for reused source date
        if req_date and req_date == source_date:
            reused_date_count += 1
            blocking_reasons.append(f"LIVE_PAPER_LABEL_KEY_REUSES_SOURCE_DATE:{run_id}")

        # Hardgate: check required_label_key exists
        if not req_date or not req_horizon:
            blocking_reasons.append(f"LIVE_PAPER_REQUIRED_LABEL_KEY_MISSING:{run_id}")
            updated_runs.append({
                **run,
                "run_status": "WAITING_FOR_LABEL",
                "required_label_key": required_key,
                "forward_labels_available": 0,
                "label_key_validated": False,
                "label_source": "",
            })
            waiting += 1
            continue

        # Check forward labels
        label_key = (req_date, req_horizon)
        label_count = forward_labels.get(label_key, 0)

        if label_count > 0 and req_date != source_date:
            new_status = "COMPLETED"
            completed += 1
            label_validated = True
        else:
            new_status = "WAITING_FOR_LABEL"
            waiting += 1
            label_validated = False
            if req_date == source_date:
                blocking_reasons.append(f"LABEL_KEY_EQUALS_SOURCE_DATE:{run_id}")

        updated_runs.append({
            **run,
            "run_status": new_status,
            "required_label_key": required_key,
            "forward_labels_available": label_count,
            "label_key_validated": label_validated,
            "label_source": "v8_forward_return_labels.json" if label_count > 0 else "",
        })

    total_active = completed + waiting
    all_completed = total_active > 0 and completed == total_active and reused_date_count == 0

    completion_status = (
        "COMPLETED" if all_completed
        else "PARTIAL_COMPLETION" if completed > 0
        else "WAITING_FOR_LABELS"
    )

    result = {
        "status": "V12_1_LIVE_PAPER_STATUS_UPDATE_BUILT",
        "active_run_count": total_active,
        "completed_run_count": completed,
        "waiting_run_count": waiting,
        "blocked_run_count": blocked,
        "all_live_paper_runs_completed": all_completed,
        "live_paper_completion_status": completion_status,
        "reused_source_date_count": reused_date_count,
        "updated_runs": updated_runs,
        "blocking_reasons": blocking_reasons if not all_completed else [],
        "ready_for_alpha_claim": False,
        "alpha_validated": False,
        "production": "BLOCKED",
        "broker_runtime": "BLOCKED",
        "real_trade": "BLOCKED",
    }

    json.dump(result, open(C / "v12_1_live_paper_status_update.json", "w"), indent=2)
    print(f"V12.1 Status: {completion_status} | completed={completed} waiting={waiting} "
          f"blocked={blocked} reused_dates={reused_date_count}")


if __name__ == "__main__":
    main()
