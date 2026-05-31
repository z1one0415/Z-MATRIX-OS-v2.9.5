# allowlist: forbidden-token-definition
"""Tests for action_queue — FIFO display-action queue, append-only JSONL"""
from __future__ import annotations

import os
import tempfile

import pytest

from zmatrix.agent.action_queue import (
    ACTION_QUEUE_PATH,
    ActionType,
    dequeue_action,
    enqueue_action,
    list_pending_actions,
    peek_next_action,
)


@pytest.fixture(autouse=True)
def _isolate_action_queue(monkeypatch):
    with tempfile.NamedTemporaryFile(mode="w", suffix=".jsonl", delete=False) as tf:
        tf.write("")
        temp_path = tf.name
    monkeypatch.setattr("zmatrix.agent.action_queue.ACTION_QUEUE_PATH", temp_path)
    yield
    if os.path.exists(temp_path):
        os.unlink(temp_path)


def test_enqueue_dequeue_cycle():
    action_id = enqueue_action(ActionType.FOCUS_TICKER.value, {"ticker": "AAPL"})
    action = dequeue_action()
    assert action is not None
    assert action["action_id"] == action_id
    assert action["action_type"] == "FOCUS_TICKER"
    assert action["payload"] == {"ticker": "AAPL"}


def test_action_queue_fifo_order():
    id1 = enqueue_action(ActionType.OPEN_CASE.value, {"case": "A"})
    id2 = enqueue_action(ActionType.OPEN_CASE.value, {"case": "B"})
    id3 = enqueue_action(ActionType.OPEN_CASE.value, {"case": "C"})

    first = dequeue_action()
    second = dequeue_action()
    third = dequeue_action()

    assert first["action_id"] == id1
    assert second["action_id"] == id2
    assert third["action_id"] == id3


def test_peek_does_not_remove():
    enqueue_action(ActionType.SHOW_HYPOTHESIS.value, {"hypothesis": "test"})
    peeked = peek_next_action()
    assert peeked is not None
    assert peeked["action_type"] == "SHOW_HYPOTHESIS"

    actual = dequeue_action()
    assert actual is not None
    assert actual["action_id"] == peeked["action_id"]


def test_list_pending_actions():
    enqueue_action(ActionType.SHOW_FACTOR_REPORT.value, {"factor": "value"})
    enqueue_action(ActionType.SHOW_ANALYSIS_ZONE.value, {"zone": "tech"})
    pending = list_pending_actions()
    assert len(pending) == 2
    assert pending[0]["action_type"] == "SHOW_FACTOR_REPORT"
    assert pending[1]["action_type"] == "SHOW_ANALYSIS_ZONE"


def test_action_queue_cannot_mutate_researchdb():
    allowed_action_types = {a.value for a in ActionType}
    assert "WRITE_RESEARCHDB" not in allowed_action_types
    assert "TRIGGER_TRADE" not in allowed_action_types
    assert "AUTO_APPROVE" not in allowed_action_types
    assert "MUTATE_DB" not in allowed_action_types
