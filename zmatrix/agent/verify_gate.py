# allowlist: forbidden-token-definition
"""Agent Verify Gate — verify executed proposals, record to audit ledger"""
from __future__ import annotations

import json
import os
import uuid
from datetime import datetime, timezone
from pathlib import Path

from .proposal_ledger import ProposalStatus, append_to_ledger, get_proposal

AUDIT_LEDGER_PATH = os.environ.get(
    "Z_AUDIT_LEDGER_PATH",
    str(Path(__file__).resolve().parent.parent.parent
        / "data" / "research_db" / "agent" / "ledgers" / "audit_ledger.jsonl"),
)

PROPOSAL_LEDGER_PATH = os.environ.get(
    "Z_PROPOSAL_LEDGER_PATH",
    str(Path(__file__).resolve().parent.parent.parent
        / "data" / "research_db" / "agent" / "ledgers" / "proposal_ledger.jsonl"),
)


def _append_audit_entry(entry: dict) -> None:
    os.makedirs(os.path.dirname(AUDIT_LEDGER_PATH), exist_ok=True)
    with open(AUDIT_LEDGER_PATH, "a", encoding="utf-8") as fh:
        fh.write(json.dumps(entry, ensure_ascii=False) + "\n")


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


def run_verify_for_proposal(proposal_id: str) -> dict:
    proposal = get_proposal(proposal_id)

    errors: list[str] = []
    warnings: list[str] = []

    changes = proposal.get("proposed_changes", {})
    if not changes:
        errors.append("No proposed_changes to verify")

    target_files = proposal.get("target_files", [])
    if not target_files:
        warnings.append("No target_files specified")

    for tf in target_files:
        if tf.endswith(".jsonl") and "write" in str(changes).lower():
            warnings.append(f"Modifying JSONL ledger {tf} outside append path")
        if "zmatrix" not in tf and tf.endswith(".py"):
            errors.append(f"Target file {tf} is outside zmatrix package")

    passed = len(errors) == 0

    if passed:
        _update_proposal_status_in_ledger(proposal_id, ProposalStatus.CLOSED.value)
        new_status = ProposalStatus.CLOSED.value
    else:
        _update_proposal_status_in_ledger(proposal_id, ProposalStatus.VERIFY_FAILED.value)
        new_status = ProposalStatus.VERIFY_FAILED.value

    verify_output = {
        "passed": passed,
        "errors": errors,
        "warnings": warnings,
        "new_status": new_status,
    }

    audit_entry = {
        "entry_id": str(uuid.uuid4()),
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "event_type": "VERIFY",
        "agent_id": proposal.get("agent_id", ""),
        "proposal_id": proposal_id,
        "details": verify_output,
        "production_allowed": False,
    }
    _append_audit_entry(audit_entry)

    return verify_output
