# allowlist: forbidden-token-definition
"""Tests for verify_gate — verify executed proposals"""
from __future__ import annotations

import os
import tempfile

import pytest

from zmatrix.agent.proposal_ledger import create_proposal, get_proposal, submit_proposal
from zmatrix.agent.approval_gate import approve_proposal
from zmatrix.agent.execution_runner import execute_approved_proposal
from zmatrix.agent.verify_gate import run_verify_for_proposal


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
    with tempfile.NamedTemporaryFile(mode="w", suffix=".jsonl", delete=False) as tf:
        tf.write("")
        temp_audit = tf.name
    monkeypatch.setattr("zmatrix.agent.proposal_ledger.PROPOSAL_LEDGER_PATH", temp_proposal)
    monkeypatch.setattr("zmatrix.agent.approval_gate.PROPOSAL_LEDGER_PATH", temp_proposal)
    monkeypatch.setattr("zmatrix.agent.approval_gate.APPROVAL_LEDGER_PATH", temp_approval)
    monkeypatch.setattr("zmatrix.agent.execution_runner.PROPOSAL_LEDGER_PATH", temp_proposal)
    monkeypatch.setattr("zmatrix.agent.execution_runner.EXECUTION_LEDGER_PATH", temp_execution)
    monkeypatch.setattr("zmatrix.agent.verify_gate.PROPOSAL_LEDGER_PATH", temp_proposal)
    monkeypatch.setattr("zmatrix.agent.verify_gate.AUDIT_LEDGER_PATH", temp_audit)
    monkeypatch.setattr("zmatrix.agent.audit_ledger.AUDIT_LEDGER_PATH", temp_audit)
    yield
    for p in (temp_proposal, temp_approval, temp_execution, temp_audit):
        if os.path.exists(p):
            os.unlink(p)


def _create_executed_proposal():
    p = create_proposal(
        agent_id="agent-1",
        command_id="cmd-1",
        target_files=["zmatrix/agent/test.py"],
        target_layers=["layer-1"],
        proposed_changes={"key": "value"},
        risk_level="R3_WRITE_RESEARCH_DB",
    )
    submit_proposal(p["proposal_id"])
    approve_proposal(p["proposal_id"], "approver-1", "ok")
    execute_approved_proposal(p["proposal_id"], dry_run=False)
    return get_proposal(p["proposal_id"])


def test_verify_passed_proposal():
    p = _create_executed_proposal()
    result = run_verify_for_proposal(p["proposal_id"])
    assert result["passed"] is True
    assert result["errors"] == []
    assert result["new_status"] == "CLOSED"

    final = get_proposal(p["proposal_id"])
    assert final["status"] == "CLOSED"


def test_verify_failed_proposal_sets_status():
    p = create_proposal(
        agent_id="agent-1",
        command_id="cmd-1",
        target_files=["not_zmatrix/file.py"],
        target_layers=["layer-1"],
        proposed_changes={},
        risk_level="R3_WRITE_RESEARCH_DB",
    )
    submit_proposal(p["proposal_id"])
    approve_proposal(p["proposal_id"], "approver-1", "ok")
    execute_approved_proposal(p["proposal_id"], dry_run=False)

    result = run_verify_for_proposal(p["proposal_id"])
    assert result["passed"] is False
    assert len(result["errors"]) > 0
    assert result["new_status"] == "VERIFY_FAILED"

    final = get_proposal(p["proposal_id"])
    assert final["status"] == "VERIFY_FAILED"


def test_verify_result_recorded():
    p = _create_executed_proposal()
    result = run_verify_for_proposal(p["proposal_id"])
    assert "passed" in result
    assert "errors" in result
    assert "warnings" in result

    from zmatrix.agent.audit_ledger import get_audit_trail
    trail = get_audit_trail(p["proposal_id"])
    assert len(trail) >= 1
    assert trail[0]["event_type"] == "VERIFY"
