"""Prompt Middleware Event Adapters — build EventStore PromptPatchEvents (no auto-append)"""
from __future__ import annotations

from zmatrix.event_store.builders import build_event


def build_prompt_patch_request_event(prompt_patch_request: dict) -> dict:
    """Build a PromptPatchEvent (subtype: PromptPatchRequest).

    Does NOT append. Does NOT write Hermes memory. Does NOT write Z9.
    Does NOT inject prompts. Does NOT write system_prompt.
    """
    payload = {
        "event_subtype": "PromptPatchRequest",
        "prompt_patch_request_id": prompt_patch_request.get("prompt_patch_request_id", ""),
        "request_version": prompt_patch_request.get("request_version", ""),
        "request_type": prompt_patch_request.get("request_type", ""),
        "approval_status": prompt_patch_request.get("approval_status", ""),
        "status": prompt_patch_request.get("status", ""),
    }
    return build_event(
        event_type="PromptPatchEvent",
        producer_module="zmatrix.prompt_middleware.event_adapters.build_prompt_patch_request_event",
        payload=payload,
    )


def build_prompt_render_preview_event(render_preview: dict) -> dict:
    """Build a PromptPatchEvent (subtype: PromptRenderPreview).

    Does NOT append. Does NOT write Hermes memory. Does NOT write Z9.
    """
    payload = {
        "event_subtype": "PromptRenderPreview",
        "render_id": render_preview.get("render_id", ""),
        "render_version": render_preview.get("render_version", ""),
        "mode": render_preview.get("mode", "PREVIEW_ONLY"),
        "render_status": render_preview.get("render_status", ""),
    }
    return build_event(
        event_type="PromptPatchEvent",
        producer_module="zmatrix.prompt_middleware.event_adapters.build_prompt_render_preview_event",
        payload=payload,
    )


def build_prompt_patch_audit_event(audit_record: dict) -> dict:
    """Build a PromptPatchEvent (subtype: PromptPatchAudit).

    Does NOT append. Does NOT write Hermes memory. Does NOT write Z9.
    """
    payload = {
        "event_subtype": "PromptPatchAudit",
        "prompt_patch_audit_id": audit_record.get("prompt_patch_audit_id", ""),
        "audit_version": audit_record.get("audit_version", ""),
        "audit_status": audit_record.get("audit_status", "PREVIEW_AUDITED"),
    }
    return build_event(
        event_type="PromptPatchEvent",
        producer_module="zmatrix.prompt_middleware.event_adapters.build_prompt_patch_audit_event",
        payload=payload,
    )
