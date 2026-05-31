# allowlist: forbidden-token-definition
"""Agent Action Queue — FIFO display-action queue, append-only JSONL"""
from __future__ import annotations

import json
import os
import uuid
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path


class ActionType(str, Enum):
    OPEN_CASE = "OPEN_CASE"
    FOCUS_TICKER = "FOCUS_TICKER"
    SHOW_EVENT_WINDOW = "SHOW_EVENT_WINDOW"
    SHOW_FACTOR_REPORT = "SHOW_FACTOR_REPORT"
    SHOW_HYPOTHESIS = "SHOW_HYPOTHESIS"
    SHOW_ANALYSIS_ZONE = "SHOW_ANALYSIS_ZONE"
    ASK_HUMAN_REVIEW = "ASK_HUMAN_REVIEW"
    SHOW_AGENT_PROPOSAL = "SHOW_AGENT_PROPOSAL"
    SHOW_VERIFY_RESULT = "SHOW_VERIFY_RESULT"
    SHOW_DATA_QUALITY_WARNING = "SHOW_DATA_QUALITY_WARNING"
    REQUEST_USER_DECISION = "REQUEST_USER_DECISION"


ACTION_QUEUE_PATH = os.environ.get(
    "Z_ACTION_QUEUE_PATH",
    str(Path(__file__).resolve().parent.parent.parent
        / "data" / "research_db" / "agent" / "action_queue.jsonl"),
)


def enqueue_action(action_type: str, payload: dict) -> str:
    action_id = str(uuid.uuid4())
    action = {
        "action_id": action_id,
        "action_type": action_type,
        "payload": payload,
        "created_at": datetime.now(timezone.utc).isoformat(),
    }
    os.makedirs(os.path.dirname(ACTION_QUEUE_PATH), exist_ok=True)
    with open(ACTION_QUEUE_PATH, "a", encoding="utf-8") as fh:
        fh.write(json.dumps(action, ensure_ascii=False) + "\n")
    return action_id


def _read_all_actions() -> list[dict]:
    if not os.path.exists(ACTION_QUEUE_PATH):
        return []
    actions: list[dict] = []
    with open(ACTION_QUEUE_PATH, "r", encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if line:
                actions.append(json.loads(line))
    return actions


def _rewrite_queue(actions: list[dict]) -> None:
    os.makedirs(os.path.dirname(ACTION_QUEUE_PATH), exist_ok=True)
    with open(ACTION_QUEUE_PATH, "w", encoding="utf-8") as fh:
        for action in actions:
            fh.write(json.dumps(action, ensure_ascii=False) + "\n")


def dequeue_action() -> dict | None:
    actions = _read_all_actions()
    if not actions:
        return None
    first = actions.pop(0)
    _rewrite_queue(actions)
    return first


def peek_next_action() -> dict | None:
    actions = _read_all_actions()
    if not actions:
        return None
    return actions[0]


def list_pending_actions() -> list[dict]:
    return _read_all_actions()
