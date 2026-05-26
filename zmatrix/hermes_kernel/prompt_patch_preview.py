"""Prompt Patch Preview — render heuristics as safe, preview-only prompt patches

This is NOT prompt auto-injection.
This is NOT system prompt modification.
This is NOT strategy modification.
This is NOT long-term memory write.
"""
from __future__ import annotations
import hashlib
from datetime import datetime, timezone

from zmatrix.hermes_kernel.schemas import HERMES_KERNEL_SAFETY

PROMPT_PATCH_PREVIEW_VERSION = "PROMPT_PATCH_PREVIEW_V10"

_FORBIDDEN_TOKENS = [
    ("BUY", "forbidden-action-token-redacted"),
    ("SELL", "forbidden-action-token-redacted"),
    ("AUTO_TRADE", "forbidden-action-token-redacted"),
    ("BROKER_ORDER", "forbidden-action-token-redacted"),
    ("MARKET_ORDER", "forbidden-action-token-redacted"),
    ("REAL_TRADE", "forbidden-action-token-redacted"),
]


def _redact_forbidden_tokens(text: str) -> str:
    for token, replacement in _FORBIDDEN_TOKENS:
        text = text.replace(token, replacement)
    return text


def build_prompt_patch_preview(
    *,
    task_context: dict,
    heuristics: list[dict],
    max_items: int = 5,
) -> dict:
    """Build a Prompt Patch Preview from task context and matched heuristics.

    Returns a preview-only patch that must NOT be auto-injected.
    Requires human approval before any use.
    """
    task_type = task_context.get("task_type", "unknown")

    # Filter active heuristics first, then limit to max_items
    active = [h for h in heuristics if h.get("status") == "ACTIVE"]
    inactive = [h for h in heuristics if h.get("status") != "ACTIVE"]
    selected = (active + inactive)[:max_items]

    # Build patch text
    lines = []
    lines.append("[Hermes Discipline Patch Preview]")
    lines.append(f"Mode: PREVIEW_ONLY")
    lines.append(f"Auto Injection: DISABLED")
    lines.append(f"Human Approval Required: TRUE")
    lines.append("")
    lines.append(f"Task: {task_type} | Ticker: {task_context.get('ticker','')}")
    lines.append("")
    lines.append("Relevant historical disciplines:")
    for i, h in enumerate(selected, 1):
        title = h.get("title", "untitled")
        conf = h.get("confidence", "UNKNOWN")
        status = h.get("status", "UNKNOWN")
        lines.append(f"  {i}. [{status}] {title} (confidence: {conf})")

    lines.append("")
    lines.append("Task-specific cautions:")
    lines.append("- Review historical patterns before making decisions")
    lines.append("- Consider confidence levels when weighting evidence")

    patch_text = "\n".join(lines)
    redacted = _redact_forbidden_tokens(patch_text)

    seed = f"{task_type}|{task_context.get('ticker','')}|{len(selected)}"
    patch_id = hashlib.sha256(seed.encode()).hexdigest()[:32]
    created_at = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    return {
        "patch_id": patch_id,
        "patch_version": PROMPT_PATCH_PREVIEW_VERSION,
        "mode": "PREVIEW_ONLY",
        "created_at": created_at,
        "task_context": dict(task_context),
        "selected_heuristics": selected,
        "prompt_patch_text": redacted,
        "heuristic_count": len(selected),
        "injection_allowed": False,
        "prompt_auto_injection_allowed": False,
        "requires_human_approval": True,
        "real_trade_allowed": False,
        "real_z9_write_allowed": False,
        "hermes_memory_write_allowed": False,
        "auto_calibration_allowed": False,
    }
