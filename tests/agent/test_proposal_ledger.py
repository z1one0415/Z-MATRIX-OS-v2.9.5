# allowlist: forbidden-token-definition
"""Tests for proposal_ledger — create, submit, status transitions, append-only"""
from __future__ import annotations

import os
import tempfile

import pytest

from zmatrix.agent.proposal_ledger import (
    PROPOSAL_LEDGER_PATH,
    ProposalStatus,
    _validate_status_transition,
    append_to_ledger,
    create_proposal,
    get_proposal,
    list_proposals,
    submit_proposal,
)


@pytest.fixture(autouse=True)
def _isolate_ledger(monkeypatch):
    with tempfile.NamedTemporaryFile(mode="w", suffix=".jsonl", delete=False) as tf:
        tf.write("")
        temp_path = tf.name
    monkeypatch.setattr("zmatrix.agent.proposal_ledger.PROPOSAL_LEDGER_PATH", temp_path)
    monkeypatch.setattr("zmatrix.agent.approval_gate.PROPOSAL_LEDGER_PATH", temp_path)
    monkeypatch.setattr("zmatrix.agent.execution_runner.PROPOSAL_LEDGER_PATH", temp_path)
    monkeypatch.setattr("zmatrix.agent.verify_gate.PROPOSAL_LEDGER_PATH", temp_path)
    yield
    if os.path.exists(temp_path):
        os.unlink(temp_path)


def test_create_proposal_returns_valid_proposal():
    result = create_proposal(
        agent_id="agent-1",
        command_id="cmd-1",
        target_files=["zmatrix/agent/test.py"],
        target_layers=["layer-1"],
        proposed_changes={"key": "value"},
        risk_level="R2_DRAFT",
    )
    assert isinstance(result, dict)
    assert "proposal_id" in result
    assert result["agent_id"] == "agent-1"
    assert result["status"] == "DRAFT"
    assert result["production_allowed"] is False


def test_proposal_status_transitions():
    assert _validate_status_transition("DRAFT", "SUBMITTED") is True
    assert _validate_status_transition("SUBMITTED", "APPROVED") is True
    assert _validate_status_transition("SUBMITTED", "REJECTED") is True
    assert _validate_status_transition("APPROVED", "EXECUTED") is True
    assert _validate_status_transition("EXECUTED", "CLOSED") is True
    assert _validate_status_transition("EXECUTED", "VERIFY_FAILED") is True

    assert _validate_status_transition("DRAFT", "APPROVED") is False
    assert _validate_status_transition("DRAFT", "EXECUTED") is False
    assert _validate_status_transition("APPROVED", "SUBMITTED") is False
    assert _validate_status_transition("CLOSED", "DRAFT") is False


def test_cannot_approve_draft_proposal_directly():
    result = create_proposal(
        agent_id="agent-1",
        command_id="cmd-1",
        target_files=["zmatrix/agent/test.py"],
        target_layers=["layer-1"],
        proposed_changes={"key": "value"},
        risk_level="R2_DRAFT",
    )

    from zmatrix.agent.approval_gate import approve_proposal
    with pytest.raises(ValueError, match="Cannot approve DRAFT"):
        approve_proposal(result["proposal_id"], "approver-1", "test approval")


def test_proposal_append_only():
    initial = list_proposals()
    initial_count = len(initial)

    create_proposal(
        agent_id="agent-1",
        command_id="cmd-1",
        target_files=["zmatrix/agent/a.py"],
        target_layers=["layer-1"],
        proposed_changes={"a": 1},
        risk_level="R0_READ",
    )
    create_proposal(
        agent_id="agent-2",
        command_id="cmd-2",
        target_files=["zmatrix/agent/b.py"],
        target_layers=["layer-2"],
        proposed_changes={"b": 2},
        risk_level="R1_ANNOTATE",
    )

    all_proposals = list_proposals()
    assert len(all_proposals) == initial_count + 2


def test_production_allowed_is_false():
    for _ in range(3):
        result = create_proposal(
            agent_id="agent-1",
            command_id="cmd-1",
            target_files=["zmatrix/agent/test.py"],
            target_layers=["layer-1"],
            proposed_changes={"key": "value"},
            risk_level="R2_DRAFT",
        )
        assert result["production_allowed"] is False
