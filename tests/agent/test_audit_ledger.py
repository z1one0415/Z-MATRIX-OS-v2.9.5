# allowlist: forbidden-token-definition
"""Tests for audit_ledger — record, trail, summary"""
from __future__ import annotations

import os
import tempfile

import pytest

from zmatrix.agent.audit_ledger import (
    get_audit_summary,
    get_audit_trail,
    record_audit_entry,
)


@pytest.fixture(autouse=True)
def _isolate_audit_ledger(monkeypatch):
    with tempfile.NamedTemporaryFile(mode="w", suffix=".jsonl", delete=False) as tf:
        tf.write("")
        temp_audit = tf.name
    monkeypatch.setattr("zmatrix.agent.audit_ledger.AUDIT_LEDGER_PATH", temp_audit)
    yield
    if os.path.exists(temp_audit):
        os.unlink(temp_audit)


def test_record_audit_entry_returns_id():
    entry_id = record_audit_entry(
        event_type="PROPOSAL_CREATED",
        agent_id="agent-1",
        proposal_id="p-1",
        details={"action": "create"},
    )
    assert isinstance(entry_id, str)
    assert len(entry_id) > 0


def test_get_audit_trail_returns_entries():
    record_audit_entry("PROPOSAL_CREATED", "agent-1", "p-1", {"step": 1})
    record_audit_entry("SUBMITTED", "agent-1", "p-1", {"step": 2})
    record_audit_entry("PROPOSAL_CREATED", "agent-2", "p-2", {"step": 3})

    trail = get_audit_trail("p-1")
    assert len(trail) == 2
    assert all(e["proposal_id"] == "p-1" for e in trail)


def test_audit_ledger_append_only():
    initial = get_audit_summary()
    initial_count = initial["total_entries"]

    record_audit_entry("EVENT_A", "agent-1", "p-1", {"x": 1})
    record_audit_entry("EVENT_B", "agent-2", "p-2", {"x": 2})

    summary = get_audit_summary()
    assert summary["total_entries"] == initial_count + 2


def test_audit_entries_have_required_fields():
    entry_id = record_audit_entry(
        event_type="E2",
        agent_id="agent-1",
        proposal_id="p-1",
        details={"data": "test"},
    )
    trail = get_audit_trail("p-1")
    entry = trail[0]

    assert "entry_id" in entry
    assert "timestamp" in entry
    assert "event_type" in entry
    assert "agent_id" in entry
    assert "proposal_id" in entry
    assert "details" in entry
    assert "production_allowed" in entry
    assert entry["production_allowed"] is False
