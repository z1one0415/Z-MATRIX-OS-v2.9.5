"""Prompt Patch Request — build request from Hermes preview + approval decision"""
from __future__ import annotations
import hashlib
from datetime import datetime, timezone

from zmatrix.prompt_middleware.schemas import (
    PROMPT_PATCH_REQUEST_TYPES,
    DEFAULT_PROMPT_MIDDLEWARE_SAFETY,
)

REQUEST_VERSION = "PROMPT_PATCH_REQUEST_V10"


def build_prompt_patch_request(
    *,
    task_context: dict,
    prompt_patch_preview: dict,
    approval_decision: dict | None = None,
    request_type: str = "TASK_DISCIPLINE_PATCH",
) -> dict:
    """Build a PromptPatchRequest.

    - Without approval_decision: approval_status = PENDING_APPROVAL
    - With approval_decision and result_status=APPROVED: APPROVED_PREVIEW
    - APPROVED_PREVIEW still does NOT enable runtime injection
    """
    if request_type not in PROMPT_PATCH_REQUEST_TYPES:
        raise ValueError(f"Invalid request_type '{request_type}'")

    preview_id = prompt_patch_preview.get("patch_id", "")
    approval_decision_id = approval_decision.get("approval_decision_id", "") if approval_decision else ""

    seed = f"{request_type}|{preview_id}|{approval_decision_id}|{task_context.get('ticker','')}"
    request_id = hashlib.sha256(seed.encode()).hexdigest()[:32]
    created_at = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    if approval_decision and approval_decision.get("result_status") == "APPROVED":
        approval_status = "APPROVED_PREVIEW"
        status = "APPROVED_PREVIEW"
    else:
        approval_status = "PENDING_APPROVAL"
        status = "PENDING_APPROVAL"

    return {
        "prompt_patch_request_id": request_id,
        "request_version": REQUEST_VERSION,
        "request_type": request_type,
        "task_context": dict(task_context),
        "prompt_patch_preview_id": preview_id,
        "prompt_patch_preview": dict(prompt_patch_preview),
        "approval_decision_id": approval_decision_id,
        "approval_status": approval_status,
        "status": status,
        "created_at": created_at,
        "safety": dict(DEFAULT_PROMPT_MIDDLEWARE_SAFETY),
    }
