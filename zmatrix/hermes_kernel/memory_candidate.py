"""Memory Candidate Preview — build memory candidate preview (DRAFT only, no write)"""
from __future__ import annotations
import hashlib
from datetime import datetime, timezone

from zmatrix.hermes_kernel.schemas import HERMES_KERNEL_SAFETY


def build_memory_candidate_preview(
    *,
    source_event_id: str,
    candidate_type: str,
    title: str,
    proposed_rule: str,
    evidence_summary: str,
    confidence: str,
    risk_of_overfitting: str,
) -> dict:
    """Build a MemoryCandidate preview (DRAFT status).

    Hard rules:
    - Default status is DRAFT
    - Must NOT be APPROVED
    - Must NOT auto-write Hermes memory
    - Must NOT auto-modify strategy
    """
    seed = f"{source_event_id}|{title}|{confidence}"
    candidate_id = hashlib.sha256(seed.encode()).hexdigest()[:32]
    created_at = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    return {
        "candidate_id": candidate_id,
        "source_event_id": source_event_id,
        "candidate_type": candidate_type,
        "title": title,
        "proposed_rule": proposed_rule,
        "evidence_summary": evidence_summary,
        "confidence": confidence,
        "risk_of_overfitting": risk_of_overfitting,
        "approval_status": "DRAFT",
        "created_at": created_at,
        "safety": dict(HERMES_KERNEL_SAFETY),
        "preview_only": True,
        "write_allowed": False,
        "hermes_memory_write_allowed": False,
    }
