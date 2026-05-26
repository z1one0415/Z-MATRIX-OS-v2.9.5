"""Core Memory Preview — build core memory preview (read-only, no write to hermes)"""
from __future__ import annotations
from datetime import datetime, timezone

from zmatrix.hermes_kernel.schemas import HERMES_KERNEL_SAFETY


def build_core_memory_preview(
    *,
    memory_id: str,
    memory_type: str,
    title: str,
    content: str,
    priority: str = "MEDIUM",
    source: str = "manual",
    created_at: str | None = None,
    valid_until: str | None = None,
    status: str = "ACTIVE",
) -> dict:
    """Build a core memory preview.

    Returns a preview dict with HERMES_KERNEL_SAFETY enforced.
    Does NOT write to hermes/memory_bank.json.
    """
    if created_at is None:
        created_at = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    memory = {
        "memory_id": memory_id,
        "memory_type": memory_type,
        "title": title,
        "content": content,
        "priority": priority,
        "source": source,
        "created_at": created_at,
        "valid_until": valid_until,
        "status": status,
    }

    return {
        "memory": memory,
        "safety": dict(HERMES_KERNEL_SAFETY),
        "preview_only": True,
        "write_allowed": False,
        "hermes_memory_write_allowed": False,
    }
