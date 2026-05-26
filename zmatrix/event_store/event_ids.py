"""Event ID generation — deterministic 32-char hex event_id + sha256 payload hash

event_id is deterministic: same event_type + canonical payload + created_at yields same id.
No random numbers used.
"""
from __future__ import annotations
import hashlib
import json


def hash_payload(payload: dict) -> str:
    """Return 64-char sha256 hex of canonical JSON sorted payload."""
    raw = json.dumps(payload, sort_keys=True, ensure_ascii=False, default=str)
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def build_event_id(
    event_type: str,
    payload: dict,
    created_at: str | None = None,
) -> str:
    """Build 32-char hex deterministic event_id.

    Deterministic over event_type + canonical payload + created_at.
    Uses sha256 truncated to first 32 hex characters.
    """
    canonical_payload = json.dumps(payload, sort_keys=True, ensure_ascii=False, default=str)
    seed = f"{event_type}|{canonical_payload}|{created_at or ''}"
    full_hash = hashlib.sha256(seed.encode("utf-8")).hexdigest()
    return full_hash[:32]
