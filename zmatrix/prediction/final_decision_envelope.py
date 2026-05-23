"""Final Decision Envelope v1.0 — G18 output wrapper with upstream constraints."""
from __future__ import annotations


def build_final_decision(prediction, g09_signal: dict | None = None) -> dict:
    """Build final decision envelope wrapping G18 prediction with upstream evidence."""
    entry = "WAIT"
    exit_intent = None

    if g09_signal and g09_signal.get("available"):
        # G09 sell signal overrides G18 buy tendency
        pos_action = g09_signal.get("position_action", "")
        if pos_action in ("SELL_TRADING_KEEP_CORE", "REDUCE_CORE", "MAJOR_REDUCE_OR_EXIT"):
            entry = "WAIT"
            exit_intent = pos_action
        else:
            entry = g09_signal.get("entry_action_cap", prediction.action_proposal)

    return {
        "version": "v1.0",
        "ticker": prediction.ticker,
        "entry_intent": entry,
        "exit_intent": exit_intent,
        "paper_action": "PAPER_TRACK" if entry in ("WATCH", "PAPER_TRACK") else None,
        "action_cap": entry,
        "g09_source": "available" if (g09_signal and g09_signal.get("available")) else "unavailable",
        "requires_z16": True,
        "requires_z17": True,
        "forbidden_real_trade_checked": True,
    }
