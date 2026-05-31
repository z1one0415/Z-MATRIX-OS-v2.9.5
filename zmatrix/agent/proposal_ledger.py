# allowlist: forbidden-token-definition
"""Agent Proposal Ledger — proposal dataclass, create/submit/query, append-only JSONL"""
from __future__ import annotations

import json
import os
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path


class ProposalStatus(str, Enum):
    DRAFT = "DRAFT"
    SUBMITTED = "SUBMITTED"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    DEFERRED = "DEFERRED"
    EXECUTED = "EXECUTED"
    VERIFY_FAILED = "VERIFY_FAILED"
    CLOSED = "CLOSED"


_VALID_TRANSITIONS = {
    ProposalStatus.DRAFT: {ProposalStatus.SUBMITTED},
    ProposalStatus.SUBMITTED: {ProposalStatus.APPROVED, ProposalStatus.REJECTED, ProposalStatus.DEFERRED},
    ProposalStatus.APPROVED: {ProposalStatus.EXECUTED},
    ProposalStatus.EXECUTED: {ProposalStatus.VERIFY_FAILED, ProposalStatus.CLOSED},
}

PROPOSAL_LEDGER_PATH = os.environ.get(
    "Z_PROPOSAL_LEDGER_PATH",
    str(Path(__file__).resolve().parent.parent.parent
        / "data" / "research_db" / "agent" / "ledgers" / "proposal_ledger.jsonl"),
)


@dataclass
class AgentProposal:
    proposal_id: str
    command_id: str
    agent_id: str
    target_files: list[str] = field(default_factory=list)
    target_layers: list[str] = field(default_factory=list)
    proposed_changes: dict = field(default_factory=dict)
    risk_level: str = "R0_READ"
    policy_result: dict = field(default_factory=dict)
    human_review_required: bool = True
    status: str = "DRAFT"
    created_at: str = ""
    production_allowed: bool = False


def _validate_status_transition(old_status: str, new_status: str) -> bool:
    old = ProposalStatus(old_status)
    new = ProposalStatus(new_status)
    return new in _VALID_TRANSITIONS.get(old, set())


def _proposal_to_dict(p: AgentProposal) -> dict:
    return {
        "proposal_id": p.proposal_id,
        "command_id": p.command_id,
        "agent_id": p.agent_id,
        "target_files": p.target_files,
        "target_layers": p.target_layers,
        "proposed_changes": p.proposed_changes,
        "risk_level": p.risk_level,
        "policy_result": p.policy_result,
        "human_review_required": p.human_review_required,
        "status": p.status,
        "created_at": p.created_at,
        "production_allowed": p.production_allowed,
    }


def append_to_ledger(proposal: dict) -> None:
    os.makedirs(os.path.dirname(PROPOSAL_LEDGER_PATH), exist_ok=True)
    with open(PROPOSAL_LEDGER_PATH, "a", encoding="utf-8") as fh:
        fh.write(json.dumps(proposal, ensure_ascii=False) + "\n")


def create_proposal(
    agent_id: str,
    command_id: str,
    target_files: list[str],
    target_layers: list[str],
    proposed_changes: dict,
    risk_level: str,
) -> dict:
    proposal_id = str(uuid.uuid4())
    now = datetime.now(timezone.utc).isoformat()
    proposal = AgentProposal(
        proposal_id=proposal_id,
        command_id=command_id,
        agent_id=agent_id,
        target_files=target_files,
        target_layers=target_layers,
        proposed_changes=proposed_changes,
        risk_level=risk_level,
        status=ProposalStatus.DRAFT.value,
        created_at=now,
        production_allowed=False,
    )
    result = _proposal_to_dict(proposal)
    append_to_ledger(result)
    return result


def submit_proposal(proposal_id: str) -> dict:
    proposals = _read_all_proposals()
    for p in proposals:
        if p["proposal_id"] == proposal_id:
            if not _validate_status_transition(p["status"], ProposalStatus.SUBMITTED.value):
                raise ValueError(
                    f"Cannot submit proposal {proposal_id}: invalid transition from {p['status']} to SUBMITTED"
                )
            p["status"] = ProposalStatus.SUBMITTED.value
            append_to_ledger(p)
            return p
    raise KeyError(f"Proposal not found: {proposal_id}")


def _read_all_proposals() -> list[dict]:
    if not os.path.exists(PROPOSAL_LEDGER_PATH):
        return []
    proposals: list[dict] = []
    with open(PROPOSAL_LEDGER_PATH, "r", encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if line:
                proposals.append(json.loads(line))
    return proposals


def _deduplicate_proposals(proposals: list[dict]) -> list[dict]:
    seen: dict[str, dict] = {}
    for p in proposals:
        pid = p["proposal_id"]
        seen[pid] = p
    return list(seen.values())


def get_proposal(proposal_id: str) -> dict:
    all_proposals = _read_all_proposals()
    for p in reversed(all_proposals):
        if p["proposal_id"] == proposal_id:
            return p
    raise KeyError(f"Proposal not found: {proposal_id}")


def list_proposals(agent_id: str | None = None, status: str | None = None) -> list[dict]:
    proposals = _deduplicate_proposals(_read_all_proposals())
    if agent_id is not None:
        proposals = [p for p in proposals if p.get("agent_id") == agent_id]
    if status is not None:
        proposals = [p for p in proposals if p.get("status") == status]
    return proposals


def _update_proposal_status(proposal_id: str, new_status: str) -> dict:
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
