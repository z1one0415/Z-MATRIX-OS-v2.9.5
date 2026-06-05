#!/usr/bin/env python3
"""V12.1: Live Paper Due Schedule — generate per-run required_label_key from live-paper dates."""
import json
from pathlib import Path

W = Path(__file__).resolve().parent.parent.parent
C = W / "runtime_reports" / "cases"


def load(name: str) -> dict:
    p = C / name
    return json.loads(p.read_text()) if p.exists() else {}


def load_forward_dates() -> list:
    """Load sorted unique as_of_dates from v8_forward_return_labels."""
    p = C / "v8_large_data" / "v8_forward_return_labels.json"
    if not p.exists():
        return []
    data = json.loads(p.read_text())
    return sorted(set(lbl.get("as_of_date", "") for lbl in data.get("labels", [])))


def find_next_date(forward_dates: list, source_date: str) -> str:
    """Find the next trading date strictly after source_date."""
    for d in forward_dates:
        if d > source_date:
            return d
    return ""  # No future date available → fail-closed


def main():
    registry = load("v12_1_live_paper_run_registry.json")
    obs_loop = load("v12_paper_observation_loop.json")
    snapshot = load("v12_research_signal_snapshot.json")
    forward_dates = load_forward_dates()

    source_date = "20240905"
    source_from_labels = source_date if source_date in forward_dates else forward_dates[0] if forward_dates else ""

    # Try to determine live_paper_start_as_of_date
    live_paper_date = find_next_date(forward_dates, source_date)
    date_resolved = bool(live_paper_date)

    blocking_reasons = []
    if not date_resolved:
        blocking_reasons.append("LIVE_PAPER_START_DATE_NOT_RESOLVED")

    schedule_items = []
    for run in registry.get("runs", []):
        if run.get("run_status") != "LIVE_PAPER_PENDING":
            continue

        horizon = run.get("horizon", "T20")

        if date_resolved:
            required_label_key = {
                "as_of_date": live_paper_date,
                "horizon": horizon,
            }
            schedule_status = "WAITING_FOR_FUTURE_LABEL"
            label_status = "NOT_YET_AVAILABLE"
        else:
            required_label_key = {
                "as_of_date": "",
                "horizon": horizon,
            }
            schedule_status = "WAITING_FOR_FUTURE_LABEL"
            label_status = "NOT_YET_AVAILABLE"

        # Hardgate: required_label_key.as_of_date MUST differ from source
        if required_label_key.get("as_of_date") == source_date:
            blocking_reasons.append("LIVE_PAPER_LABEL_KEY_REUSES_SOURCE_DATE")
            schedule_status = "WAITING_FOR_FUTURE_LABEL"
            label_status = "NOT_YET_AVAILABLE"

        item = {
            "live_paper_run_id": run["live_paper_run_id"],
            "research_signal_id": run.get("research_signal_id", ""),
            "factor_id": run.get("factor_id", ""),
            "horizon": horizon,
            "source_start_as_of_date": source_date,
            "live_paper_start_as_of_date": live_paper_date if date_resolved else "",
            "required_label_horizon": horizon,
            "required_label_key": required_label_key,
            "required_label_status": label_status,
            "schedule_status": schedule_status,
            "paper_only": True,
            "investment_action": "NONE",
            "trade_action": "NONE",
        }
        schedule_items.append(item)

    ready = date_resolved and "LIVE_PAPER_LABEL_KEY_REUSES_SOURCE_DATE" not in blocking_reasons

    result = {
        "status": "V12_1_LIVE_PAPER_DUE_SCHEDULE_BUILT",
        "scheduled_run_count": len(schedule_items),
        "waiting_for_future_label_count": len(schedule_items),
        "live_paper_start_date_resolved": date_resolved,
        "live_paper_start_as_of_date": live_paper_date if date_resolved else "",
        "ready_for_completion": ready,
        "schedule_items": schedule_items,
        "blocking_reasons": ["LIVE_PAPER_FUTURE_LABELS_NOT_AVAILABLE"] + blocking_reasons if not ready else [],
        "ready_for_alpha_claim": False,
        "alpha_validated": False,
        "production": "BLOCKED",
        "broker_runtime": "BLOCKED",
        "real_trade": "BLOCKED",
    }

    json.dump(result, open(C / "v12_1_live_paper_due_schedule.json", "w"), indent=2)
    print(f"V12.1 Due Schedule: {len(schedule_items)} scheduled | date_resolved={date_resolved} "
          f"live_paper_date={live_paper_date} | ready={ready}")


if __name__ == "__main__":
    main()
