"""MemoryCandidate Preview — build from EventStore outcome/mistake/review events

MemoryCandidate is a DRAFT only.
Does NOT write Hermes.
Does NOT write Z9.
Does NOT enter long-term memory.
Does NOT modify strategy.
"""
from __future__ import annotations
import hashlib
from datetime import datetime, timezone

MEMORY_CANDIDATE_PREVIEW_VERSION = "MEMORY_CANDIDATE_PREVIEW_V10"

MEMORY_CANDIDATE_STATUS = frozenset({
    "DRAFT", "PENDING_REVIEW", "APPROVED", "REJECTED",
    "QUARANTINED", "EXPIRED", "SUPERSEDED",
})


def build_memory_candidate_preview(
    *,
    source_event: dict,
    attribution: dict,
    proposed_lesson: str,
) -> dict:
    """Build a MemoryCandidate Preview from a source event + attribution.

    - Default status is DRAFT
    - Must NOT produce APPROVED status
    - Does NOT write Hermes
    """
    seed = f"{source_event.get('event_id','')}|{attribution.get('mistake_type','')}|{proposed_lesson}"
    candidate_id = hashlib.sha256(seed.encode()).hexdigest()[:32]
    created_at = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    status = "DRAFT"
    requires_human_approval = True

    return {
        "memory_candidate_id": candidate_id,
        "candidate_version": MEMORY_CANDIDATE_PREVIEW_VERSION,
        "source_event_id": source_event.get("event_id", ""),
        "mistake_type": attribution.get("mistake_type", "unknown"),
        "severity": attribution.get("severity", "LOW"),
        "confidence": attribution.get("confidence", "LOW"),
        "proposed_lesson": proposed_lesson,
        "evidence_event_ids": attribution.get("evidence_event_ids", []),
        "status": status,
        "requires_human_approval": requires_human_approval,
        "created_at": created_at,
        "write_allowed": False,
        "hermes_memory_write_allowed": False,
        "real_z9_write_allowed": False,
        "auto_calibration_allowed": False,
        "real_trade_allowed": False,
    }
