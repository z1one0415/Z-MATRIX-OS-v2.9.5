"""CalibrationEvent Preview — build calibration event preview from MemoryCandidate

CalibrationEvent in this version is PREVIEW ONLY.
Does NOT auto-tune parameters.
Does NOT modify B/R/D.
Does NOT modify Z8.
Does NOT modify G18.
Does NOT write long-term memory.
"""
from __future__ import annotations
import hashlib
from datetime import datetime, timezone

CALIBRATION_EVENT_PREVIEW_VERSION = "CALIBRATION_EVENT_PREVIEW_V10"

TARGET_DOMAINS = frozenset({
    "B_MATRIX", "R_MATRIX", "D_MATRIX", "Z8_POSITION_CONTROL",
    "G18_DECISION", "PROMPT_DISCIPLINE", "ACCOUNT_CONSTITUTION", "UNKNOWN",
})


def build_calibration_event_preview(
    *,
    memory_candidate: dict,
    target_domain: str,
    proposed_change: dict,
) -> dict:
    """Build a CalibrationEvent Preview from a MemoryCandidate.

    - auto_apply_allowed MUST be False
    - auto_calibration_allowed MUST be False
    - requires_human_approval MUST be True
    """
    seed = f"{memory_candidate.get('memory_candidate_id','')}|{target_domain}"
    calibration_id = hashlib.sha256(seed.encode()).hexdigest()[:32]
    created_at = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    if target_domain not in TARGET_DOMAINS:
        target_domain = "UNKNOWN"

    return {
        "calibration_event_id": calibration_id,
        "calibration_version": CALIBRATION_EVENT_PREVIEW_VERSION,
        "memory_candidate_id": memory_candidate.get("memory_candidate_id", ""),
        "target_domain": target_domain,
        "proposed_change": dict(proposed_change),
        "status": "PENDING_HUMAN_APPROVAL",
        "auto_apply_allowed": False,
        "auto_calibration_allowed": False,
        "requires_human_approval": True,
        "created_at": created_at,
        "real_trade_allowed": False,
        "real_z9_write_allowed": False,
        "hermes_memory_write_allowed": False,
    }
