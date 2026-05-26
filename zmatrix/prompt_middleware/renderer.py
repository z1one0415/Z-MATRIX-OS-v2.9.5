"""Prompt Middleware Renderer — render prompt patch preview (no runtime injection)"""
from __future__ import annotations
import hashlib
from datetime import datetime, timezone

from zmatrix.prompt_middleware.schemas import DEFAULT_PROMPT_MIDDLEWARE_SAFETY

RENDER_VERSION = "PROMPT_MIDDLEWARE_RENDER_PREVIEW_V10"


def render_prompt_patch_preview(
    *,
    prompt_patch_request: dict,
    base_prompt_preview: str = "",
) -> dict:
    """Render a prompt patch as a middleware preview.

    The output is a PREVIEW_ONLY rendering.
    It does NOT modify real system prompts.
    It does NOT inject into OpenClaw runtime.
    """
    preview = prompt_patch_request.get("prompt_patch_preview", {})
    patch_text = preview.get("prompt_patch_text", "")
    task_type = prompt_patch_request.get("request_type", "UNKNOWN")
    ticker = prompt_patch_request.get("task_context", {}).get("ticker", "")

    lines = []
    lines.append("[BASE PROMPT PREVIEW]")
    lines.append(base_prompt_preview if base_prompt_preview else "(no base prompt provided)")
    lines.append("")
    lines.append("[HERMES PATCH PREVIEW - NOT INJECTED]")
    lines.append(patch_text if patch_text else "(no patch text)")
    lines.append("")
    lines.append("[SAFETY]")
    lines.append("Mode: PREVIEW_ONLY")
    lines.append("Runtime Injection: DISABLED")
    lines.append("System Prompt Write: DISABLED")
    lines.append("Human Approval Required: TRUE")
    lines.append(f"Task: {task_type} | Ticker: {ticker}")

    rendered = "\n".join(lines)

    seed = f"{prompt_patch_request.get('prompt_patch_request_id','')}|{base_prompt_preview[:50]}"
    render_id = hashlib.sha256(seed.encode()).hexdigest()[:32]
    created_at = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    return {
        "render_id": render_id,
        "render_version": RENDER_VERSION,
        "mode": "PREVIEW_ONLY",
        "prompt_patch_request_id": prompt_patch_request.get("prompt_patch_request_id", ""),
        "base_prompt_preview": base_prompt_preview,
        "rendered_prompt_preview": rendered,
        "patch_text": patch_text,
        "render_status": "RENDERED_PREVIEW",
        "created_at": created_at,
        "system_prompt_write_allowed": False,
        "runtime_injection_allowed": False,
        "prompt_auto_injection_allowed": False,
        "requires_human_approval": True,
        "real_trade_allowed": False,
        "real_z9_write_allowed": False,
        "hermes_memory_write_allowed": False,
        "auto_calibration_allowed": False,
    }
