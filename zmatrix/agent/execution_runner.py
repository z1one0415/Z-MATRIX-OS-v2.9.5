# allowlist: forbidden-token-definition
"""Agent Execution Runner — execute approved proposals with dry-run gating"""
from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from pathlib import Path

from .proposal_ledger import ProposalStatus, append_to_ledger, get_proposal

EXECUTION_LEDGER_PATH = os.environ.get(
    "Z_EXECUTION_LEDGER_PATH",
    str(Path(__file__).resolve().parent.parent.parent
        / "data" / "research_db" / "agent" / "ledgers" / "execution_ledger.jsonl"),
)

PROPOSAL_LEDGER_PATH = os.environ.get(
    "Z_PROPOSAL_LEDGER_PATH",
    str(Path(__file__).resolve().parent.parent.parent
        / "data" / "research_db" / "agent" / "ledgers" / "proposal_ledger.jsonl"),
)


def _append_execution_entry(entry: dict) -> None:
    os.makedirs(os.path.dirname(EXECUTION_LEDGER_PATH), exist_ok=True)
    with open(EXECUTION_LEDGER_PATH, "a", encoding="utf-8") as fh:
        fh.write(json.dumps(entry, ensure_ascii=False) + "\n")


def _dry_run_proposal(proposal: dict) -> dict:
    errors: list[str] = []
    target_files = proposal.get("target_files", [])
    for tf in target_files:
        if not tf.endswith(".py"):
            errors.append(f"Target file {tf} is not a .py file")

    target_layers = proposal.get("target_layers", [])
    if not target_layers:
        errors.append("No target_layers specified")

    return {
        "passed": len(errors) == 0,
        "errors": errors,
    }


def _update_proposal_status_in_ledger(proposal_id: str, new_status: str) -> dict:
    from .proposal_ledger import _read_all_proposals, _validate_status_transition
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


def execute_approved_proposal(proposal_id: str, dry_run: bool = True) -> dict:
    proposal = get_proposal(proposal_id)

    if proposal.get("status") != ProposalStatus.APPROVED.value:
        return {
            "status": "BLOCKED",
            "output": {},
            "dry_run": dry_run,
            "errors": [f"Proposal {proposal_id} is not APPROVED (current: {proposal.get('status')})"],
        }

    dry_result = _dry_run_proposal(proposal)

    if not dry_result["passed"]:
        return {
            "status": "DRY_RUN_FAILED",
            "output": {},
            "dry_run": dry_run,
            "errors": dry_result["errors"],
        }

    if dry_run:
        entry = {
            "execution_id": f"exec-{proposal_id}",
            "proposal_id": proposal_id,
            "dry_run": True,
            "status": "DRY_RUN_PASSED",
            "output": {"message": "Dry run passed"},
            "errors": [],
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
        _append_execution_entry(entry)
        return {
            "status": "DRY_RUN_PASSED",
            "output": {"message": "Dry run passed"},
            "dry_run": True,
            "errors": [],
        }

    _update_proposal_status_in_ledger(proposal_id, ProposalStatus.EXECUTED.value)

    entry = {
        "execution_id": f"exec-{proposal_id}",
        "proposal_id": proposal_id,
        "dry_run": False,
        "status": "EXECUTED",
        "output": proposal.get("proposed_changes", {}),
        "errors": [],
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
    _append_execution_entry(entry)

    return {
        "status": "EXECUTED",
        "output": proposal.get("proposed_changes", {}),
        "dry_run": False,
        "errors": [],
    }
