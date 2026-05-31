# allowlist: forbidden-token-definition
"""Agent Audit Ledger — record and query audit trail, append-only JSONL"""
from __future__ import annotations

import json
import os
import uuid
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

AUDIT_LEDGER_PATH = os.environ.get(
    "Z_AUDIT_LEDGER_PATH",
    str(Path(__file__).resolve().parent.parent.parent
        / "data" / "research_db" / "agent" / "ledgers" / "audit_ledger.jsonl"),
)


def record_audit_entry(
    event_type: str,
    agent_id: str,
    proposal_id: str,
    details: dict,
) -> str:
    entry_id = str(uuid.uuid4())
    entry = {
        "entry_id": entry_id,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "event_type": event_type,
        "agent_id": agent_id,
        "proposal_id": proposal_id,
        "details": details,
        "production_allowed": False,
    }
    os.makedirs(os.path.dirname(AUDIT_LEDGER_PATH), exist_ok=True)
    with open(AUDIT_LEDGER_PATH, "a", encoding="utf-8") as fh:
        fh.write(json.dumps(entry, ensure_ascii=False) + "\n")
    return entry_id


def get_audit_trail(proposal_id: str) -> list[dict]:
    if not os.path.exists(AUDIT_LEDGER_PATH):
        return []
    entries: list[dict] = []
    with open(AUDIT_LEDGER_PATH, "r", encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            entry = json.loads(line)
            if entry.get("proposal_id") == proposal_id:
                entries.append(entry)
    return entries


def get_audit_summary() -> dict:
    if not os.path.exists(AUDIT_LEDGER_PATH):
        return {
            "total_entries": 0,
            "by_type": {},
            "by_agent": {},
        }
    entries: list[dict] = []
    with open(AUDIT_LEDGER_PATH, "r", encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            entries.append(json.loads(line))

    type_counter: Counter = Counter()
    agent_counter: Counter = Counter()
    for e in entries:
        type_counter[e.get("event_type", "UNKNOWN")] += 1
        agent_counter[e.get("agent_id", "UNKNOWN")] += 1

    return {
        "total_entries": len(entries),
        "by_type": dict(type_counter),
        "by_agent": dict(agent_counter),
    }
