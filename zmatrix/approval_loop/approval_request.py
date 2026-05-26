"""Approval Request — build approval request (PENDING_REVIEW only)"""
from __future__ import annotations
import hashlib
from datetime import datetime, timezone

from zmatrix.approval_loop.schemas import APPROVAL_REQUEST_TYPES, DEFAULT_APPROVAL_SAFETY

APPROVAL_REQUEST_VERSION = "APPROVAL_REQUEST_V10"


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
    - Does NOT write Hermes memory
    - Does NOT write Z9
    """
    if request_type not in APPROVAL_REQUEST_TYPES:
        raise ValueError(f"Invalid request_type '{request_type}'. Must be one of {APPROVAL_REQUEST_TYPES}")

    if not source_preview:
        raise ValueError("source_preview must not be empty")

    seed = f"{request_type}|{source_preview.get('source_event_id', '')}|{reason}"
    request_id = hashlib.sha256(seed.encode()).hexdigest()[:32]
    created_at = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    return {
        "approval_request_id": request_id,
        "request_version": APPROVAL_REQUEST_VERSION,
        "request_type": request_type,
        "source_preview_id": source_preview.get("candidate_id") or source_preview.get("memory_candidate_id") or source_preview.get("patch_id", ""),
        "source_preview": dict(source_preview),
        "requested_by": requested_by,
        "reason": reason,
        "status": "PENDING_REVIEW",
        "requires_human_approval": True,
        "created_at": created_at,
        "safety": dict(DEFAULT_APPROVAL_SAFETY),
    }
