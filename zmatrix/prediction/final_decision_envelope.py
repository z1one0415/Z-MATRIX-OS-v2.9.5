"""Final Decision Envelope v1.2 — G18 output with enforced priority rules + fast risk overlay.

Priority: G09 sell > G09 hard_blocks > FAST_RISK_OVERLAY > G18 probability > G11 warn > G14 provenance
G11: STRONG_WARNING_ONLY, never hard veto
Z16/G17: required confirmations for any paper action
Fast risk overlay: veto power over PAPER_TRACK regardless of base_score
No BUY/SELL/AUTO_TRADE/MARKET_ORDER ever
"""
from __future__ import annotations
from zmatrix.action.action_contracts import assert_no_real_trade
from zmatrix.prediction.fast_risk_overlay import (
    evaluate_fast_risk_overlay,
    MarketSnapshot,
    FastRiskResult,
)


_ORDER = ["AVOID", "BLOCKED", "WAIT", "WATCH", "PAPER_PROBE_ELIGIBLE_PENDING_Z16_Z17", "PAPER_TRACK", "PAPER_PROBE_ELIGIBLE"]

def _lowest_cap(lhs, rhs):
    """Return the more conservative action cap."""
    for a in _ORDER:
        if lhs == a or rhs == a: return a
    return lhs


def build_final_decision(prediction, upstream_evidence: dict | None = None,
                         market_snapshot: "MarketSnapshot | None" = None) -> dict:
    up = upstream_evidence or {}
    g09 = up.get("g09", {})
    g11 = up.get("g11", {})
    g14 = up.get("g14", {})
    g08 = up.get("g08", {})
    z16 = up.get("z16", {})
    g17 = up.get("g17", {})

    entry = prediction.action_proposal or "WAIT"
    exit_intent = None
    paper_action = None
    blocking_reasons = []
    risk_warnings = list(g11.get("warnings", []))
    required_confirmations = []

    # ── Rule 1: G09 sell_decision overrides G18 buy ──
    pos_action = ""
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

    # ── Conflict resolution ──
    from zmatrix.prediction.conflict_resolver import resolve_upstream_conflicts
    conflict = resolve_upstream_conflicts(up, prediction)
    if conflict["suggested_action_cap"] in ("WAIT", "WATCH"):
        entry = conflict["suggested_action_cap"]
    entry = _lowest_cap(entry, conflict["suggested_action_cap"])

    # ── Rule 5b: Fast Risk Overlay (v1.2) ──
    fast_risk = None
    if market_snapshot is not None:
        base_score = int(prediction.probability * 100)
        fast_risk = evaluate_fast_risk_overlay(market_snapshot, base_score=base_score)
        if not fast_risk.paper_track_allowed:
            if paper_action == "PAPER_TRACK":
                paper_action = None
            if entry in ("PAPER_TRACK", "PAPER_PROBE_ELIGIBLE"):
                entry = _lowest_cap(entry, "WAIT")
        # Apply action from fast risk if more conservative
        fr_action = fast_risk.recommended_action
        if fr_action in ("WAIT", "REDUCE_OR_WAIT", "AVOID"):
            entry = _lowest_cap(entry, "WAIT")

    # ── Rule 6: Forbidden real trade ──
    assert_no_real_trade(entry)
    if exit_intent:
        assert_no_real_trade(exit_intent)

    return {
        "decision_version": "v1.2",
        "version": "v1.2",
        "ticker": prediction.ticker,
        "conflict_resolution": conflict,
        "conflicts": conflict["conflicts"],
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
            "z16": {
                "required": z16.get("required", "Z16_PRICE_GATE" in required_confirmations),
                "available": z16.get("available", False),
                "status": z16.get("status"),
                "source": z16.get("source", "Z16_PRICE_GATE"),
                "warnings": z16.get("warnings", []),
            },
            "g17": {
                "required": g17.get("required", "G17_ACCOUNT_CONFIRMATION" in required_confirmations),
                "available": g17.get("available", False),
                "status": g17.get("status"),
                "source": g17.get("source", "G17_ACCOUNT_CONFIRMATION"),
                "warnings": g17.get("warnings", []),
            },
        },
        "forbidden_real_trade_checked": True,
        "fast_risk_overlay": {
            "evaluated": fast_risk is not None,
            "triggered_gates": fast_risk.triggered_gates if fast_risk else [],
            "total_penalty": fast_risk.total_penalty if fast_risk else 0,
            "final_score": fast_risk.final_score if fast_risk else None,
            "final_score_cap": fast_risk.final_score_cap if fast_risk else None,
            "paper_track_allowed": fast_risk.paper_track_allowed if fast_risk else True,
            "recommended_action": fast_risk.recommended_action if fast_risk else None,
            "action_gate_reason": fast_risk.action_gate_reason if fast_risk else "",
        },
    }
