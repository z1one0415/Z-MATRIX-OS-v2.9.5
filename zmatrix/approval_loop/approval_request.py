"""Approval Request — build approval request (PENDING_REVIEW only)"""
from __future__ import annotations
import hashlib
import json
from datetime import datetime, timezone

from zmatrix.approval_loop.schemas import APPROVAL_REQUEST_TYPES, DEFAULT_APPROVAL_SAFETY

APPROVAL_REQUEST_VERSION = "APPROVAL_REQUEST_V10"


def _extract_source_preview_id(source_preview: dict) -> str:
    """Extract the canonical preview ID from a source_preview dict.

    Order of precedence:
    1. memory_candidate_id (MemoryCandidatePreview)
    2. calibration_event_id (CalibrationEventPreview)
    3. patch_id (PromptPatchPreview)
    4. candidate_id (legacy)
    5. source_preview_id (generic fallback)
    """
    return (
        source_preview.get("memory_candidate_id")
        or source_preview.get("calibration_event_id")
        or source_preview.get("patch_id")
        or source_preview.get("candidate_id")
        or source_preview.get("source_preview_id")
        or ""
    )


def _hash_source_preview(source_preview: dict) -> str:
    """Deterministic hash of the full source_preview for uniqueness."""
    return hashlib.sha256(
        json.dumps(source_preview, sort_keys=True, ensure_ascii=False).encode("utf-8")
    ).hexdigest()


def build_approval_request(
    *,
    request_type: str,
    source_preview: dict,
    requested_by: str = "HermesMemoryKernel",
    reason: str = "",
) -> dict:
    """Build an ApprovalRequest.

    - request_type must be in APPROVAL_REQUEST_TYPES
    - status is always PENDING_REVIEW
    - source_preview_id supports memory_candidate_id / calibration_event_id / patch_id
    - request_id includes source_preview_hash to prevent collision
    - Does NOT write Hermes memory
    - Does NOT write Z9
    """
    if request_type not in APPROVAL_REQUEST_TYPES:
        raise ValueError(f"Invalid request_type '{request_type}'. Must be one of {APPROVAL_REQUEST_TYPES}")

    if not source_preview:
        raise ValueError("source_preview must not be empty")

    source_preview_id = _extract_source_preview_id(source_preview)
    source_preview_hash = _hash_source_preview(source_preview)

    seed = f"{request_type}|{source_preview_id}|{source_preview_hash}|{requested_by}|{reason}"
    request_id = hashlib.sha256(seed.encode()).hexdigest()[:32]
    created_at = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    return {
        "approval_request_id": request_id,
        "request_version": APPROVAL_REQUEST_VERSION,
        "request_type": request_type,
        "source_preview_id": source_preview_id,
        "source_preview_hash": source_preview_hash,
        "source_preview": dict(source_preview),
        "requested_by": requested_by,
        "reason": reason,
        "status": "PENDING_REVIEW",
        "requires_human_approval": True,
        "created_at": created_at,
        "safety": dict(DEFAULT_APPROVAL_SAFETY),
    }
