"""Final Decision Envelope v2.0 — G18 context-aware output with interpretation layers.

v2.0: Added probability_interpretation, position_management, event_risk_interpretation.
Priority unchanged: G09 sell > G09 hard_blocks > FAST_RISK_OVERLAY > G18 probability > G11 warn > G14 provenance
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
    for a in _ORDER:
        if lhs == a or rhs == a: return a
    return lhs

def _probability_bucket(p: float) -> str:
    if p >= 0.70: return "STRONG_RESEARCH_SIGNAL"
    if p >= 0.50: return "MODERATE_RESEARCH_SIGNAL"
    return "WEAK_OR_NEGATIVE_RESEARCH_SIGNAL"

def _event_interpretation(snap: MarketSnapshot | None) -> dict:
    if snap is None:
        return {"event_active": False}
    return {
        "event_active": snap.event_window_active,
        "event_type": snap.event_type,
        "event_risk_severity": snap.event_risk_severity,
        "event_phase": snap.event_phase,
        "scheduled_event_policy": "reduce_interpretation_strength_not_global_stop",
    }

def _position_interpretation(snap: MarketSnapshot | None, fast_risk: FastRiskResult | None) -> dict:
    if snap is None:
        return {"status": "NO_POSITION"}
    flags = fast_risk.position_management_flags if fast_risk else []
    return {
        "position_state": snap.position_state,
        "shares": snap.shares,
        "avg_holding_cost": snap.avg_holding_cost,
        "review_flags": [f.get("gate") for f in flags],
        "oversold_review_eligible": any("R11" in f.get("gate", "") for f in flags),
        "not_new_entry_signal": True,
        "not_auto_add_signal": True,
    }

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

    # ── Rule 1: G09 sell ──
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

    # ── Rule 2: G09 hard_blocks ──
    if g09 and (g09.get("hard_blocks") or (g09.get("sell_decision") or {}).get("hard_blocks")):
        entry = "WAIT"
        paper_action = None
        blocking_reasons.append("G09_HARD_BLOCKS")

    # ── Rule 3: G11 warning only ──

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

    # ── Fast Risk Overlay ──
    fast_risk = None
    if market_snapshot is not None:
        base_score = int(prediction.probability * 100)
        fast_risk = evaluate_fast_risk_overlay(market_snapshot, base_score=base_score)
        if not fast_risk.paper_track_allowed:
            if paper_action == "PAPER_TRACK":
                paper_action = None
            if entry in ("PAPER_TRACK", "PAPER_PROBE_ELIGIBLE"):
                entry = _lowest_cap(entry, "WAIT")
        fr_action = fast_risk.recommended_action
        if fr_action in ("WAIT", "REDUCE_OR_WAIT", "AVOID"):
            entry = _lowest_cap(entry, "WAIT")

    # ── Rule 6: Forbidden real trade ──
    assert_no_real_trade(entry)
    if exit_intent:
        assert_no_real_trade(exit_intent)

    # ── v2.0: interpretation layers ──
    prob = prediction.probability
    return {
        "decision_version": "v2.0",
        "version": "v2.0",
        "ticker": prediction.ticker,
        "conflict_resolution": conflict,
        "conflicts": conflict["conflicts"],
        "entry_intent": entry,
        "exit_intent": exit_intent,
        "paper_action": paper_action,
        "action_cap": entry,
        "probability_after_constraints": prob,
        "required_confirmations": required_confirmations,
        "risk_warnings": risk_warnings,
        "blocking_reasons": blocking_reasons,
        "probability_interpretation": {
            "raw_probability": prob,
            "conviction_bucket": _probability_bucket(prob),
            "label_is_action_cap": True,
            "allowed_action_is_not_trade": True,
        },
        "position_management": _position_interpretation(market_snapshot, fast_risk),
        "event_risk_interpretation": _event_interpretation(market_snapshot),
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
        "board_regime_context": {
            "available": False,
            "board_type": None,
            "regime_state": None,
            "strategy_family": None,
            "b_matrix_search_status": None,
            "action_interpretation": None,
        },
        "fast_risk_overlay": {
            "evaluated": fast_risk is not None,
            "triggered_gates": fast_risk.triggered_gates if fast_risk else [],
            "total_penalty": fast_risk.total_penalty if fast_risk else 0,
            "final_score": fast_risk.final_score if fast_risk else None,
            "final_score_cap": fast_risk.final_score_cap if fast_risk else None,
            "paper_track_allowed": fast_risk.paper_track_allowed if fast_risk else True,
            "recommended_action": fast_risk.recommended_action if fast_risk else None,
            "action_gate_reason": fast_risk.action_gate_reason if fast_risk else "",
            "position_management_flags": fast_risk.position_management_flags if fast_risk else [],
        },
    }
