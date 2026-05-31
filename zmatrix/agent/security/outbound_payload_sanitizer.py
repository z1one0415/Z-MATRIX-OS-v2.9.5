# allowlist: forbidden-token-definition
"""Outbound Payload Sanitizer — redacts secrets from outbound payloads"""
from __future__ import annotations

import json
import re

SECRET_KEY_NAMES = [
    "OPENAI_API_KEY",
    "ANTHROPIC_API_KEY",
    "GOOGLE_API_KEY",
    "GEMINI_API_KEY",
    "DEEPSEEK_API_KEY",
    "GITHUB_TOKEN",
    "BROKER_TOKEN",
    "EMAIL_TOKEN",
    "COOKIE",
    "Authorization",
    "Bearer",
]

KEY_PATTERN = re.compile(r'(sk-|sk-ant-|AIza|xai-|hf_)[a-zA-Z0-9_-]{10,}', re.IGNORECASE)

REDACTED = "***REDACTED***"


def _redact_value(val: str) -> str:
    if KEY_PATTERN.search(val):
        return REDACTED
    return val


def _redact_dict(obj: dict) -> dict:
    result = {}
    for key, value in obj.items():
        if any(name.lower() in key.lower() for name in SECRET_KEY_NAMES):
            if isinstance(value, str):
                result[key] = REDACTED
            else:
                result[key] = value
        elif isinstance(value, dict):
            result[key] = _redact_dict(value)
        elif isinstance(value, list):
            result[key] = [_redact_item(v) for v in value]
        elif isinstance(value, str):
            result[key] = _redact_value(value)
        else:
            result[key] = value
    return result


def _redact_item(item):
    if isinstance(item, dict):
        return _redact_dict(item)
    if isinstance(item, str):
        return _redact_value(item)
    return item


def sanitize_payload(payload: dict | str) -> dict:
    if isinstance(payload, str):
        try:
            payload = json.loads(payload)
        except (json.JSONDecodeError, TypeError):
            return {"raw": REDACTED}
    return _redact_dict(payload)


def contains_secret(payload: dict | str) -> bool:
    if isinstance(payload, str):
        text = payload
    else:
        text = json.dumps(payload, ensure_ascii=False)
    for name in SECRET_KEY_NAMES:
        if name.lower() in text.lower():
            return True
    if KEY_PATTERN.search(text):
        return True
    return False


def block_if_account_raw(payload: dict | str) -> dict:
    if isinstance(payload, str):
        text = payload
    else:
        text = json.dumps(payload, ensure_ascii=False)
    if "account/raw" in text or "account\\raw" in text:
        return {"blocked": True, "reason": "payload references account/raw data"}
    return {"blocked": False, "reason": ""}
