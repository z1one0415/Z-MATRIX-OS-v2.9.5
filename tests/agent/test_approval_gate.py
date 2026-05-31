# allowlist: forbidden-token-definition
"""Tests for approval_gate — evaluate, approve, reject"""
from __future__ import annotations

import os
import tempfile

import pytest

from zmatrix.agent.proposal_ledger import create_proposal, get_proposal, submit_proposal
from zmatrix.agent.approval_gate import (
    approve_proposal,
    evaluate_approval_requirement,
    reject_proposal,
)


@pytest.fixture(autouse=True)
def _isolate_ledgers(monkeypatch):
    with tempfile.NamedTemporaryFile(mode="w", suffix=".jsonl", delete=False) as tf:
        tf.write("")
        temp_proposal = tf.name
    with tempfile.NamedTemporaryFile(mode="w", suffix=".jsonl", delete=False) as tf:
        tf.write("")
        temp_approval = tf.name
    monkeypatch.setattr("zmatrix.agent.proposal_ledger.PROPOSAL_LEDGER_PATH", temp_proposal)
    monkeypatch.setattr("zmatrix.agent.approval_gate.PROPOSAL_LEDGER_PATH", temp_proposal)
    monkeypatch.setattr("zmatrix.agent.approval_gate.APPROVAL_LEDGER_PATH", temp_approval)
    monkeypatch.setattr("zmatrix.agent.execution_runner.PROPOSAL_LEDGER_PATH", temp_proposal)
    monkeypatch.setattr("zmatrix.agent.verify_gate.PROPOSAL_LEDGER_PATH", temp_proposal)
    yield
    for p in (temp_proposal, temp_approval):
        if os.path.exists(p):
            os.unlink(p)


def test_evaluate_approval_r0_no_approval_needed():
    proposal = {
        "proposal_id": "p-1",
        "risk_level": "R0_READ",
    }
    result = evaluate_approval_requirement(proposal)
    assert result["requires_approval"] is False
    assert result["requires_human_approval"] is False


def test_evaluate_approval_r1_no_approval_needed():
    proposal = {
        "proposal_id": "p-1",
        "risk_level": "R1_ANNOTATE",
    }
    result = evaluate_approval_requirement(proposal)
    assert result["requires_approval"] is False
    assert result["requires_human_approval"] is False


def test_evaluate_approval_r2_auto_approval():
    proposal = {
        "proposal_id": "p-1",
        "risk_level": "R2_DRAFT",
    }
    result = evaluate_approval_requirement(proposal)
    assert result["requires_approval"] is False


def test_evaluate_approval_r3_requires_approval():
    proposal = {
        "proposal_id": "p-1",
        "risk_level": "R3_WRITE_RESEARCH_DB",
    }
    result = evaluate_approval_requirement(proposal)
    assert result["requires_approval"] is True
    assert result["requires_human_approval"] is False


def test_evaluate_approval_r4_requires_human():
    proposal = {
        "proposal_id": "p-1",
        "risk_level": "R4_CODE_PATCH_PROPOSAL",
    }
    result = evaluate_approval_requirement(proposal)
    assert result["requires_approval"] is True
    assert result["requires_human_approval"] is True


def test_evaluate_approval_r5_requires_human():
    proposal = {
        "proposal_id": "p-1",
        "risk_level": "R5_RELEASE_PROPOSAL",
    }
    result = evaluate_approval_requirement(proposal)
    assert result["requires_approval"] is True
    assert result["requires_human_approval"] is True


def test_evaluate_approval_r9_cannot_be_approved():
    proposal = {
        "proposal_id": "p-1",
        "risk_level": "R9_FORBIDDEN",
    }
    result = evaluate_approval_requirement(proposal)
    assert result["requires_approval"] is True
    assert result["requires_human_approval"] is True
    assert "cannot be approved" in result["reason"].lower()


def test_approve_proposal_changes_status():
    p = create_proposal(
        agent_id="agent-1",
        command_id="cmd-1",
        target_files=["zmatrix/agent/test.py"],
        target_layers=["layer-1"],
        proposed_changes={"key": "value"},
        risk_level="R4_CODE_PATCH_PROPOSAL",
    )
    submitted = submit_proposal(p["proposal_id"])
    assert submitted["status"] == "SUBMITTED"

    approved = approve_proposal(p["proposal_id"], "approver-1", "looks good")
    assert approved["status"] == "APPROVED"


def test_cannot_approve_r9():
    p = create_proposal(
        agent_id="agent-1",
        command_id="cmd-1",
        target_files=["zmatrix/agent/test.py"],
        target_layers=["layer-1"],
        proposed_changes={"key": "value"},
        risk_level="R9_FORBIDDEN",
    )
    submit_proposal(p["proposal_id"])

    with pytest.raises(ValueError, match="R9_FORBIDDEN"):
        approve_proposal(p["proposal_id"], "approver-1", "should not work")


def test_reject_proposal():
    p = create_proposal(
        agent_id="agent-1",
        command_id="cmd-1",
        target_files=["zmatrix/agent/test.py"],
        target_layers=["layer-1"],
        proposed_changes={"key": "value"},
        risk_level="R3_WRITE_RESEARCH_DB",
    )
    submit_proposal(p["proposal_id"])

    rejected = reject_proposal(p["proposal_id"], "approver-1", "not safe")
    assert rejected["status"] == "REJECTED"


def test_cannot_approve_already_rejected():
    p = create_proposal(
        agent_id="agent-1",
        command_id="cmd-1",
        target_files=["zmatrix/agent/test.py"],
        target_layers=["layer-1"],
        proposed_changes={"key": "value"},
        risk_level="R3_WRITE_RESEARCH_DB",
    )
    submit_proposal(p["proposal_id"])
    reject_proposal(p["proposal_id"], "approver-1", "no")

    with pytest.raises(ValueError, match="invalid transition"):
        approve_proposal(p["proposal_id"], "approver-1", "try again")
