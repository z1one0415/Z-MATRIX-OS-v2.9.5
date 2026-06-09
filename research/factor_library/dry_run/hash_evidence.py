"""
Hash Evidence — Compute SHA-256 hashes for noop evidence.

Computation only. No persistent writes. No file I/O.
"""

from __future__ import annotations

import hashlib
import json


def compute_hash_only_evidence(payload: dict) -> str:
    """
    Compute a SHA-256 hash of a JSON-serializable payload.

    This is a pure computation — no file writes, no persistence,
    no network access.

    Args:
        payload: Any JSON-serializable dict.

    Returns:
        Hex digest of the SHA-256 hash.
    """
    raw = json.dumps(payload, sort_keys=True, ensure_ascii=False).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()
