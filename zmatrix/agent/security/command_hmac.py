# allowlist: forbidden-token-definition
"""Command HMAC — HMAC-SHA256 signing and verification for command envelopes"""
from __future__ import annotations

import hashlib
import hmac
import json
import os

DEFAULT_SECRET = os.environ.get("Z_COMMAND_HMAC_SECRET", "zmatrix-agent-hmac-secret")


def compute_hmac(envelope: dict, secret_key: str = "") -> str:
    key = (secret_key or DEFAULT_SECRET).encode("utf-8")
    payload = json.dumps(envelope, sort_keys=True, ensure_ascii=False).encode("utf-8")
    return hmac.new(key, payload, hashlib.sha256).hexdigest()


def verify_hmac(envelope: dict, hmac_value: str, secret_key: str = "") -> bool:
    key = (secret_key or DEFAULT_SECRET).encode("utf-8")
    payload = json.dumps(envelope, sort_keys=True, ensure_ascii=False).encode("utf-8")
    expected = hmac.new(key, payload, hashlib.sha256).hexdigest()
    return hmac.compare_digest(expected, hmac_value)
