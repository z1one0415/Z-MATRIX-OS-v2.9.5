"""Final Decision Envelope v1.1 — G18 output with enforced priority rules.

Priority: G09 sell > G09 hard_blocks > G18 probability > G11 warn > G14 provenance
G11: STRONG_WARNING_ONLY, never hard veto
Z16/G17: required confirmations for any paper action
No BUY/SELL/AUTO_TRADE/MARKET_ORDER ever
"""
from __future__ import annotations
from zmatrix.action.action_contracts import assert_no_real_trade


def build_final_decision(prediction, upstream_evidence: dict | None = None) -> dict:
    up = upstream_evidence or {}
    g09 = up.get("g09", {})
    g11 = up.get("g11", {})
    g14 = up.get("g14", {})
    g08 = up.get("g08", {})

    entry = prediction.action_proposal or "WAIT"
    exit_intent = None
    paper_action = None
    blocking_reasons = []
    risk_warnings = list(g11.get("warnings", []))
    required_confirmations = []

    # ── Rule 1: G09 sell_decision overrides G18 buy ──
    g09_avail = g09.get("available") is True or g09.get("status") in ("PASS", "DEGRADED")
    if g09 and g09_avail:
        sell = g09.get("sell_decision") or {}
        pos_action = g09.get("position_action") or sell.get("position_action", "")
        sell_actions = ("REDUCE_CORE", "MAJOR_REDUCE_OR_EXIT", "SELL_TRADING_KEEP_CORE", "LIGHTEN_TRADING")
        if pos_action in sell_actions:
            entry = "WAIT"
            exit_intent = pos_action
            blocking_reasons.append("G09_SELL_DECISION_ACTIVE")

    # ── Rule 2: G09 hard_blocks prevent paper entry ──
    if g09 and (g09.get("hard_blocks") or (g09.get("sell_decision") or {}).get("hard_blocks")):
        entry = "WAIT"
        paper_action = None
        blocking_reasons.append("G09_HARD_BLOCKS")

    # ── Rule 3: G11 warning only, never hard veto ──
    # (risk_warnings already populated, no action change)

    # ── Rule 5: Paper actions require Z16/G17 ──
    if entry in ("WATCH", "PAPER_TRACK", "PAPER_PROBE_ELIGIBLE", "PAPER_PROBE_ELIGIBLE_PENDING_Z16_Z17"):
        required_confirmations = ["Z16_PRICE_GATE", "G17_ACCOUNT_CONFIRMATION"]
        if not blocking_reasons:
            paper_action = "PAPER_TRACK"

    # ── Rule 6: Forbidden real trade ──
    assert_no_real_trade(entry)
    if exit_intent:
        assert_no_real_trade(exit_intent)

    return {
        "decision_version": "v1.1",
        "version": "v1.1",
        "ticker": prediction.ticker,
        "entry_intent": entry,
        "exit_intent": exit_intent,
        "paper_action": paper_action,
        "action_cap": entry,
        "probability_after_constraints": prediction.probability,
        "required_confirmations": required_confirmations,
        "risk_warnings": risk_warnings,
        "blocking_reasons": blocking_reasons,
        "provenance": {
            "g09": {
                "available": g09_avail, "source": g09.get("source", "targeted_scan"),
                "version": g09.get("version"), "status": g09.get("status"),
                "r_score": g09.get("r_score"), "r_resonance_status": g09.get("r_resonance_status"),
                "r_action_cap": g09.get("r_action_cap"), "position_action": pos_action,
                "hard_blocks": g09.get("hard_blocks", []),
            },
            "g08": {"available": g08.get("available", False)},
            "g11": {"risk_authority": g11.get("risk_authority", "STRONG_WARNING_ONLY")},
            "g14": {"role": g14.get("role", "GLOBAL_BASELINE_ONLY")},
            "z16": {"required": "Z16_PRICE_GATE" in required_confirmations},
            "g17": {"required": "G17_ACCOUNT_CONFIRMATION" in required_confirmations},
        },
        "forbidden_real_trade_checked": True,
    }
