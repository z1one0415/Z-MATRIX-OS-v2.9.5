# allowlist: forbidden-token-definition
"""Payload Digest — SHA256 integrity verification for payloads"""
from __future__ import annotations

import hashlib
import json


def compute_payload_digest(payload: dict | str) -> str:
    if isinstance(payload, dict):
        data = json.dumps(payload, sort_keys=True, ensure_ascii=False).encode("utf-8")
    else:
        data = payload.encode("utf-8")
    return hashlib.sha256(data).hexdigest()


def verify_payload_integrity(payload: dict | str, expected_digest: str) -> bool:
    actual = compute_payload_digest(payload)
    return hmac.compare_digest(actual, expected_digest)
