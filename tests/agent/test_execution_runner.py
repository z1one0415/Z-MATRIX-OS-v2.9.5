# allowlist: forbidden-token-definition
"""Tests for execution_runner — execute approved proposals"""
from __future__ import annotations

import os
import tempfile

import pytest

from zmatrix.agent.proposal_ledger import create_proposal, get_proposal, submit_proposal
from zmatrix.agent.approval_gate import approve_proposal
from zmatrix.agent.execution_runner import execute_approved_proposal


@pytest.fixture(autouse=True)
def _isolate_ledgers(monkeypatch):
    with tempfile.NamedTemporaryFile(mode="w", suffix=".jsonl", delete=False) as tf:
        tf.write("")
        temp_proposal = tf.name
    with tempfile.NamedTemporaryFile(mode="w", suffix=".jsonl", delete=False) as tf:
        tf.write("")
        temp_approval = tf.name
    with tempfile.NamedTemporaryFile(mode="w", suffix=".jsonl", delete=False) as tf:
        tf.write("")
        temp_execution = tf.name
    monkeypatch.setattr("zmatrix.agent.proposal_ledger.PROPOSAL_LEDGER_PATH", temp_proposal)
    monkeypatch.setattr("zmatrix.agent.approval_gate.PROPOSAL_LEDGER_PATH", temp_proposal)
    monkeypatch.setattr("zmatrix.agent.approval_gate.APPROVAL_LEDGER_PATH", temp_approval)
    monkeypatch.setattr("zmatrix.agent.execution_runner.PROPOSAL_LEDGER_PATH", temp_proposal)
    monkeypatch.setattr("zmatrix.agent.execution_runner.EXECUTION_LEDGER_PATH", temp_execution)
    monkeypatch.setattr("zmatrix.agent.verify_gate.PROPOSAL_LEDGER_PATH", temp_proposal)
    yield
    for p in (temp_proposal, temp_approval, temp_execution):
        if os.path.exists(p):
            os.unlink(p)


def _create_approved_proposal(risk_level="R3_WRITE_RESEARCH_DB"):
    p = create_proposal(
        agent_id="agent-1",
        command_id="cmd-1",
        target_files=["zmatrix/agent/test.py"],
        target_layers=["layer-1"],
        proposed_changes={"key": "value"},
        risk_level=risk_level,
    )
    submit_proposal(p["proposal_id"])
    approve_proposal(p["proposal_id"], "approver-1", "ok")
    return get_proposal(p["proposal_id"])


def test_unapproved_proposal_blocked():
    p = create_proposal(
        agent_id="agent-1",
        command_id="cmd-1",
        target_files=["zmatrix/agent/test.py"],
        target_layers=["layer-1"],
        proposed_changes={"key": "value"},
        risk_level="R0_READ",
    )
    result = execute_approved_proposal(p["proposal_id"])
    assert result["status"] == "BLOCKED"
    assert "not APPROVED" in result["errors"][0]


def test_approved_proposal_dry_run_works():
    p = _create_approved_proposal()
    result = execute_approved_proposal(p["proposal_id"], dry_run=True)
    assert result["status"] == "DRY_RUN_PASSED"
    assert result["dry_run"] is True


def test_dry_run_failure_blocks_real():
    p = create_proposal(
        agent_id="agent-1",
        command_id="cmd-1",
        target_files=["zmatrix/agent/test.txt"],
        target_layers=[],
        proposed_changes={"key": "value"},
        risk_level="R3_WRITE_RESEARCH_DB",
    )
    submit_proposal(p["proposal_id"])
    approve_proposal(p["proposal_id"], "approver-1", "ok")
    approved = get_proposal(p["proposal_id"])

    result = execute_approved_proposal(approved["proposal_id"], dry_run=True)
    assert result["status"] == "DRY_RUN_FAILED"

    result_real = execute_approved_proposal(approved["proposal_id"], dry_run=False)
    assert result_real["status"] == "DRY_RUN_FAILED"


def test_execute_writes_to_ledger():
    p = _create_approved_proposal("R3_WRITE_RESEARCH_DB")
    result = execute_approved_proposal(p["proposal_id"], dry_run=False)
    assert result["status"] == "EXECUTED"
    assert result["dry_run"] is False

    from zmatrix.agent.proposal_ledger import get_proposal as gp
    final = gp(p["proposal_id"])
    assert final["status"] == "EXECUTED"
