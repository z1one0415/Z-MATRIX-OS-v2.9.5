# allowlist: forbidden-token-definition
"""Agent Approval Gate — evaluate, approve, reject proposals"""
from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from pathlib import Path

from .proposal_ledger import (
    ProposalStatus,
    _validate_status_transition,
    _read_all_proposals,
    append_to_ledger,
    get_proposal,
)

APPROVAL_LEDGER_PATH = os.environ.get(
    "Z_APPROVAL_LEDGER_PATH",
    str(Path(__file__).resolve().parent.parent.parent
        / "data" / "research_db" / "agent" / "ledgers" / "approval_ledger.jsonl"),
)

PROPOSAL_LEDGER_PATH = os.environ.get(
    "Z_PROPOSAL_LEDGER_PATH",
    str(Path(__file__).resolve().parent.parent.parent
        / "data" / "research_db" / "agent" / "ledgers" / "proposal_ledger.jsonl"),
)

_RISK_NUMERIC = {
    "R0_READ": 0,
    "R1_ANNOTATE": 1,
    "R2_DRAFT": 2,
    "R3_WRITE_RESEARCH_DB": 3,
    "R4_CODE_PATCH_PROPOSAL": 4,
    "R5_RELEASE_PROPOSAL": 5,
    "R9_FORBIDDEN": 9,
}


def _risk_num(level: str) -> int:
    return _RISK_NUMERIC.get(level, 0)


def evaluate_approval_requirement(proposal: dict) -> dict:
    risk_level = proposal.get("risk_level", "R0_READ")
    risk_num = _risk_num(risk_level)

    if risk_level == "R9_FORBIDDEN":
        return {
            "requires_approval": True,
            "requires_human_approval": True,
            "reason": "R9_FORBIDDEN cannot be approved under any circumstances",
        }

    if risk_num <= 1:
        return {
            "requires_approval": False,
            "requires_human_approval": False,
            "reason": f"R0-R1: no approval needed for {risk_level}",
        }

    if risk_num == 2:
        return {
            "requires_approval": False,
            "requires_human_approval": False,
            "reason": f"R2: auto-approval allowed for {risk_level}",
        }

    if risk_num == 3:
        return {
            "requires_approval": True,
            "requires_human_approval": False,
            "reason": f"R3: requires approval (policy-based) for {risk_level}",
        }

    if risk_num in (4, 5):
        return {
            "requires_approval": True,
            "requires_human_approval": True,
            "reason": f"R4/R5: requires human approval for {risk_level}",
        }

    return {
        "requires_approval": True,
        "requires_human_approval": True,
        "reason": f"Unknown risk level {risk_level}, defaulting to human approval",
    }


def _append_approval_entry(entry: dict) -> None:
    os.makedirs(os.path.dirname(APPROVAL_LEDGER_PATH), exist_ok=True)
    with open(APPROVAL_LEDGER_PATH, "a", encoding="utf-8") as fh:
        fh.write(json.dumps(entry, ensure_ascii=False) + "\n")


def _update_proposal_status_in_ledger(proposal_id: str, new_status: str) -> dict:
    proposals = _read_all_proposals()
    for p in reversed(proposals):
        if p["proposal_id"] == proposal_id:
            if not _validate_status_transition(p["status"], new_status):
                raise ValueError(
                    f"Cannot transition proposal {proposal_id} from {p['status']} to {new_status}"
                )
            p["status"] = new_status
            append_to_ledger(p)
            return p
    raise KeyError(f"Proposal not found: {proposal_id}")


def approve_proposal(proposal_id: str, approver: str, reason: str) -> dict:
    proposal = get_proposal(proposal_id)

    if proposal.get("risk_level") == "R9_FORBIDDEN":
        raise ValueError("R9_FORBIDDEN proposals cannot be approved under any circumstances")

    if proposal.get("status") == ProposalStatus.DRAFT.value:
        raise ValueError(f"Cannot approve DRAFT proposal {proposal_id}: must be SUBMITTED first")

    if not _validate_status_transition(proposal["status"], ProposalStatus.APPROVED.value):
        raise ValueError(
            f"Cannot approve proposal {proposal_id}: invalid transition from {proposal['status']} to APPROVED"
        )

    updated = _update_proposal_status_in_ledger(proposal_id, ProposalStatus.APPROVED.value)

    approval_entry = {
        "approval_id": f"approval-{proposal_id}",
        "proposal_id": proposal_id,
        "approver": approver,
        "reason": reason,
        "status": ProposalStatus.APPROVED.value,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
    _append_approval_entry(approval_entry)

    return updated


def reject_proposal(proposal_id: str, approver: str, reason: str) -> dict:
    proposal = get_proposal(proposal_id)

    if not _validate_status_transition(proposal["status"], ProposalStatus.REJECTED.value):
        raise ValueError(
            f"Cannot reject proposal {proposal_id}: invalid transition from {proposal['status']} to REJECTED"
        )

    updated = _update_proposal_status_in_ledger(proposal_id, ProposalStatus.REJECTED.value)

    approval_entry = {
        "approval_id": f"approval-{proposal_id}",
        "proposal_id": proposal_id,
        "approver": approver,
        "reason": reason,
        "status": ProposalStatus.REJECTED.value,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
    _append_approval_entry(approval_entry)

    return updated
