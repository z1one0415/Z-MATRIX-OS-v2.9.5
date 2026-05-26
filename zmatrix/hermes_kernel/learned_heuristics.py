"""Learned Heuristics Preview — build heuristic preview (read-only, no write to hermes)"""
from __future__ import annotations
from datetime import datetime, timezone

from zmatrix.hermes_kernel.schemas import HERMES_KERNEL_SAFETY


def build_learned_heuristic_preview(
    *,
    source_event_id: str,
    title: str,
    rule: str,
    scope: dict,
    confidence: str,
    evidence_count: int,
    last_validated_at: str | None = None,
) -> dict:
    """Build a learned heuristic preview.

    Returns a preview dict with HERMES_KERNEL_SAFETY enforced.
    Does NOT auto-add to long-term memory.
    Does NOT auto-inject prompts.
    """
    import hashlib
    seed = f"{source_event_id}|{title}|{confidence}|{evidence_count}"
    heuristic_id = hashlib.sha256(seed.encode()).hexdigest()[:16]

    if last_validated_at is None:
        last_validated_at = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    heuristic = {
        "heuristic_id": heuristic_id,
        "source_event_id": source_event_id,
        "title": title,
        "rule": rule,
        "scope": dict(scope),
        "confidence": confidence,
        "evidence_count": evidence_count,
        "last_validated_at": last_validated_at,
        "status": "ACTIVE",
    }

    return {
        "heuristic": heuristic,
        "safety": dict(HERMES_KERNEL_SAFETY),
        "preview_only": True,
        "write_allowed": False,
    }
