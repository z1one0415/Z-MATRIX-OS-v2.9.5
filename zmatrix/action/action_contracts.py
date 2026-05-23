"""Action Contract v1.0 — unified action semantics across all pipelines.

entry_intent: what the system thinks about entering a position
exit_intent: what the system thinks about exiting/managing a position
paper_action: paper-level execution signals (never real)
forbidden: actions that must never appear in any pipeline output
"""
from __future__ import annotations

ENTRY_INTENT = frozenset({
    "BLOCKED", "WAIT", "WATCH", "PAPER_TRACK", "PAPER_PROBE_ELIGIBLE",
})

EXIT_INTENT = frozenset({
    "HOLD_CORE", "HOLD_PROFIT", "HOLD_WAIT_CONFIRM", "HOLD_LOSS",
    "SELL_TRADING_KEEP_CORE", "REDUCE_CORE", "MAJOR_REDUCE_OR_EXIT",
    "LIGHTEN_TRADING", "STOP_REVIEW", "PARTIAL_HARVEST", "NO_POSITION",
})

PAPER_ACTION = frozenset({
    "PAPER_TRACK", "PAPER_PROBE_CONDITIONAL",
})

FORBIDDEN_REAL_ACTIONS = frozenset({
    "BUY", "SELL", "ADD", "CLEAR", "AUTO_TRADE", "MARKET_ORDER",
})


def validate_action(action: str) -> bool:
    """Returns True if action is not forbidden."""
    return action not in FORBIDDEN_REAL_ACTIONS


def assert_no_real_trade(action: str):
    """Raises ValueError if action is a real trade command."""
    if action in FORBIDDEN_REAL_ACTIONS:
        raise ValueError(f"Real trade action forbidden: {action}")
