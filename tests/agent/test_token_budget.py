# allowlist: forbidden-token-definition
"""Tests for token_budget — estimate, enforce, get_default"""
from __future__ import annotations

from zmatrix.agent.token_budget import (
    estimate_tokens,
    enforce_token_budget,
    get_default_budget,
)


class TestEstimateTokens:
    def test_estimate_tokens_returns_positive_int(self):
        result = estimate_tokens("Hello World")
        assert isinstance(result, int)
        assert result > 0

    def test_estimate_tokens_empty_string_returns_one(self):
        result = estimate_tokens("")
        assert result == 1

    def test_estimate_tokens_reasonable_approximation(self):
        text = "abcdefgh"  # 8 chars, ~2 tokens
        result = estimate_tokens(text)
        assert result == 2

    def test_estimate_tokens_long_text(self):
        text = "x" * 1000  # 1000 chars, ~250 tokens
        result = estimate_tokens(text)
        assert result == 250


class TestEnforceTokenBudget:
    def test_enforce_token_budget_within_budget_allowed(self):
        result = enforce_token_budget({"key": "short value"}, budget=4000)
        assert result["allowed"] is True
        assert result["over_budget"] is False

    def test_enforce_token_budget_over_budget_not_allowed(self):
        payload = {"data": "x" * 10000}
        result = enforce_token_budget(payload, budget=50)
        assert result["allowed"] is False
        assert result["over_budget"] is True

    def test_enforce_token_budget_returns_estimated_tokens(self):
        result = enforce_token_budget({"key": "hello"}, budget=4000)
        assert "estimated_tokens" in result
        assert isinstance(result["estimated_tokens"], int)
        assert result["estimated_tokens"] > 0


class TestGetDefaultBudget:
    def test_get_default_budget_returns_4000(self):
        result = get_default_budget()
        assert result == 4000
        assert isinstance(result, int)
