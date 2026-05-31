# allowlist: forbidden-token-definition
"""Token Budget — estimation and enforcement"""
from __future__ import annotations


def estimate_tokens(text: str) -> int:
    if not text:
        return 1
    return max(1, len(text) // 4)


def enforce_token_budget(payload: dict, budget: int) -> dict:
    text = str(payload)
    estimated = estimate_tokens(text)
    over_budget = estimated > budget

    return {
        "allowed": not over_budget,
        "estimated_tokens": estimated,
        "budget": budget,
        "over_budget": over_budget,
    }


def get_default_budget() -> int:
    return 4000
