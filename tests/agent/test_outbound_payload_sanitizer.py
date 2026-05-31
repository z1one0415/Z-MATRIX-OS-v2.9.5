# allowlist: forbidden-token-definition
"""Tests for outbound_payload_sanitizer — secret redaction and account/raw blocking"""
from __future__ import annotations

import json

from zmatrix.agent.security.outbound_payload_sanitizer import (
    REDACTED,
    block_if_account_raw,
    contains_secret,
    sanitize_payload,
)


def test_sanitize_removes_api_key():
    payload = {"messages": [{"role": "user", "content": "hello"}], "api_key": "sk-abc123secret"}
    result = sanitize_payload(payload)
    assert result.get("api_key") == REDACTED


def test_contains_secret_detects_bearer():
    payload = {"headers": {"Authorization": "Bearer tok_abcdef1234567890"}}
    assert contains_secret(payload) is True


def test_sanitize_preserves_clean_data():
    payload = {"symbol": "AAPL", "price": 150.25, "volume": 1000000}
    result = sanitize_payload(payload)
    assert result["symbol"] == "AAPL"
    assert result["price"] == 150.25
    assert result["volume"] == 1000000


def test_block_if_account_raw():
    payload = {"source": "data/research_db/account/raw/positions.csv"}
    result = block_if_account_raw(payload)
    assert result["blocked"] is True
    assert "account/raw" in result["reason"]


def test_multiple_patterns_redacted():
    payload = {
        "OPENAI_API_KEY": "sk-proj-1234567890abcdef",
        "GITHUB_TOKEN": "ghp_abcdef1234567890",
        "normal_field": "keep_me",
    }
    result = sanitize_payload(payload)
    assert result.get("OPENAI_API_KEY") == REDACTED
    assert result.get("GITHUB_TOKEN") == REDACTED
    assert result.get("normal_field") == "keep_me"
