"""Prompt Patch Audit — build audit record for prompt middleware preview"""
from __future__ import annotations
import hashlib
from datetime import datetime, timezone


def build_prompt_patch_audit_record(
    *,
    prompt_patch_request: dict,
    render_preview: dict,
    audit_note: str = "",
) -> dict:
    """Build a PromptPatchAudit record.

    Audit records are preview-only metadata.
    They do NOT enable runtime injection or system_prompt write.
    """
    seed = f"{prompt_patch_request.get('prompt_patch_request_id','')}|{render_preview.get('render_id','')}|{audit_note}"
    audit_id = hashlib.sha256(seed.encode()).hexdigest()[:32]
    created_at = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    return {
        "prompt_patch_audit_id": audit_id,
        "audit_version": "PROMPT_PATCH_AUDIT_V10",
        "prompt_patch_request_id": prompt_patch_request.get("prompt_patch_request_id", ""),
        "render_id": render_preview.get("render_id", ""),
        "audit_note": audit_note,
        "audit_status": "PREVIEW_AUDITED",
        "created_at": created_at,
        "runtime_injection_allowed": False,
        "system_prompt_write_allowed": False,
        "prompt_auto_injection_allowed": False,
        "hermes_memory_write_allowed": False,
        "real_z9_write_allowed": False,
        "real_trade_allowed": False,
    }
