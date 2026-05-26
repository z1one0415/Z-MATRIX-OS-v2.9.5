"""EventStore exporters — JSONL export/load (local only, no network)"""
from __future__ import annotations
import json
from pathlib import Path


def export_events_to_jsonl(events: list[dict], path: str) -> dict:
    """Export events to a JSONL file.

    Returns {"exported": int, "path": str}.
    No network. No Z9 write. No Hermes memory write.
    """
    path_obj = Path(path)
    path_obj.parent.mkdir(parents=True, exist_ok=True)

    count = 0
    with open(path_obj, "w", encoding="utf-8") as f:
        for event in events:
            f.write(json.dumps(event, sort_keys=True, ensure_ascii=False) + "\n")
            count += 1

    return {"exported": count, "path": str(path_obj)}


def load_events_from_jsonl(path: str) -> list[dict]:
    """Load events from a JSONL file.

    Returns list of event dicts.
    """
    events: list[dict] = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                events.append(json.loads(line))
    return events
