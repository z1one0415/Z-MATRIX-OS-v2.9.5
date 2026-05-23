"""Final Decision Envelope v1.0 — G18 output wrapper with upstream constraints."""
from __future__ import annotations
from zmatrix.action.action_contracts import assert_no_real_trade


def build_final_decision(prediction, upstream_evidence: dict | None = None) -> dict:
    up = upstream_evidence or {}
    g09 = up.get("g09", {})
    g11 = up.get("g11", {})
    g14 = up.get("g14", {})

    entry = prediction.action_proposal or "WAIT"
    exit_intent = None

    # G09 sell overrides G18 buy
    if g09 and g09.get("available"):
        pos_action = g09.get("position_action", "")
        if pos_action in ("REDUCE_CORE", "MAJOR_REDUCE_OR_EXIT", "SELL_TRADING_KEEP_CORE"):
            entry = "WAIT"
            exit_intent = pos_action
        else:
            entry = g09.get("entry_action_cap", entry)

    # Sanity check
    assert_no_real_trade(entry)
    if exit_intent:
        assert_no_real_trade(exit_intent)

    return {
        "version": "v1.0",
        "ticker": prediction.ticker,
        "entry_intent": entry,
        "exit_intent": exit_intent,
        "paper_action": "PAPER_TRACK" if entry in ("WATCH", "PAPER_TRACK") else None,
        "action_cap": entry,
        "risk_warnings": g11.get("warnings", []),
        "provenance": {
            "g09": {"available": g09.get("available", False), "source": "targeted_scan"},
            "g08": {"available": False},
            "g11": {"risk_authority": g11.get("risk_authority", "STRONG_WARNING_ONLY")},
            "g14": {"role": g14.get("role", "GLOBAL_BASELINE_ONLY")},
        },
        "requires_z16": True,
        "requires_z17": True,
        "forbidden_real_trade_checked": True,
    }