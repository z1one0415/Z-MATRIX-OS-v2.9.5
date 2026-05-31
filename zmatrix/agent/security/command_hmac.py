# allowlist: forbidden-token-definition
"""Command HMAC — HMAC-SHA256 signing and verification for command envelopes

Security: No default secret. Secret must be set via Z_COMMAND_HMAC_SECRET env var
or passed explicitly as secret_key parameter. Raise ValueError if both are empty.
"""
from __future__ import annotations

import hashlib
import hmac
import json
import os


def _get_secret(secret_key: str = "") -> str:
    key = secret_key or os.environ.get("Z_COMMAND_HMAC_SECRET", "")
    if not key:
        raise ValueError(
            "HMAC secret not set: provide secret_key or set Z_COMMAND_HMAC_SECRET"
        )
    return key


def compute_hmac(envelope: dict, secret_key: str = "") -> str:
    key = _get_secret(secret_key).encode("utf-8")
    payload = json.dumps(envelope, sort_keys=True, ensure_ascii=False).encode("utf-8")
    return hmac.new(key, payload, hashlib.sha256).hexdigest()


def verify_hmac(envelope: dict, hmac_value: str, secret_key: str = "") -> bool:
    key = _get_secret(secret_key).encode("utf-8")
    payload = json.dumps(envelope, sort_keys=True, ensure_ascii=False).encode("utf-8")
    expected = hmac.new(key, payload, hashlib.sha256).hexdigest()
    return hmac.compare_digest(expected, hmac_value)
