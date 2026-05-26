"""Tail-Risk Controller — aggregate all gates and produce final policy preview"""
from __future__ import annotations
import hashlib
from datetime import datetime, timezone

from zmatrix.tail_risk.schemas import DEFAULT_TAIL_RISK_SAFETY, TAIL_RISK_STATE
from zmatrix.tail_risk.market_signals import normalize_market_signals
from zmatrix.tail_risk.limit_down_blackhole import evaluate_limit_down_blackhole
from zmatrix.tail_risk.domestic_liquidity_crash import evaluate_domestic_liquidity_crash
from zmatrix.tail_risk.hibernate_mode import evaluate_hibernate_mode
from zmatrix.tail_risk.wakeup_probation import evaluate_wakeup_probation
from zmatrix.tail_risk.d_matrix_freeze import evaluate_d_matrix_freeze
from zmatrix.tail_risk.risk_isolation_unit import build_risk_isolation_preview

CONTROLLER_VERSION = "TAIL_RISK_CONTROLLER_PREVIEW_V10"

_STATE_RANK = {s: i for i, s in enumerate(["NORMAL", "CAUTION", "STRESS", "CRASH", "HIBERNATE"])}


def build_tail_risk_controller_preview(
    *,
    market_signals: dict,
    candidate_context: dict | None = None,
    ticker_context: dict | None = None,
    position_context: dict | None = None,
    previous_state: str = "NORMAL",
) -> dict:
    """Aggregate all tail-risk gates and produce a policy preview.

    Preview-only. No broker order. No real trade. No Hermes write.
    """
    signals = normalize_market_signals(market_signals)
    cc = candidate_context or {}
    tc = ticker_context or {}
    pc = position_context or {}

    # Evaluate all gates
    g1 = evaluate_limit_down_blackhole(market_signals=signals, ticker_context=tc)
    g2 = evaluate_domestic_liquidity_crash(market_signals=signals)
    g3 = evaluate_hibernate_mode(market_signals=signals)
    g4 = evaluate_wakeup_probation(market_signals=signals, previous_state=previous_state)
    g5 = evaluate_d_matrix_freeze(candidate_context=cc, market_signals=signals)

    gates = [g1, g2, g3, g4, g5]

    # Determine final state (highest severity wins)
    final_state = "NORMAL"
    final_decision = "ALLOW"
    for g in gates:
        gs = g.get("state", "NORMAL")
        gd = g.get("decision", "ALLOW")
        if _STATE_RANK.get(gs, 0) > _STATE_RANK.get(final_state, 0):
            final_state = gs
            final_decision = gd

    # Risk isolation
    isolation = {}
    if final_decision == "ISOLATE":
        isolation = build_risk_isolation_preview(source_result=g1, position_context=pc)

    # Action policy
    freeze_new = any(g.get("freeze_new_entries") for g in gates)
    freeze_add = final_state in ("CRASH", "HIBERNATE", "WAKEUP_PROBATION")
    d_matrix_allowed = not any(
        g.get("gate_type") in ("D_MATRIX_FREEZE", "DOMESTIC_LIQUIDITY_CRASH")
        and g.get("decision") in ("FREEZE", "ISOLATE") for g in gates
    )
    requires_review = any(g.get("requires_human_review") for g in gates)

    seed = f"{previous_state}|{final_state}|{signals.get('hard_gate_pass_rate','')}"
    cid = hashlib.sha256(seed.encode()).hexdigest()[:32]
    created_at = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    return {
        "controller_id": cid,
        "controller_version": CONTROLLER_VERSION,
        "mode": "PREVIEW_ONLY",
        "created_at": created_at,
        "final_state": final_state,
        "final_decision": final_decision,
        "action_policy_preview": {
            "allow_new_entry": not freeze_new,
            "allow_add_position": not freeze_add,
            "allow_d_matrix": d_matrix_allowed,
            "allow_watch_only": True,
            "requires_human_review": requires_review,
        },
        "gate_results": gates,
        "risk_isolation_preview": isolation,
        "real_trade_allowed": False,
        "broker_order_allowed": False,
        "auto_buy_allowed": False,
        "auto_sell_allowed": False,
        "auto_position_close_allowed": False,
        "safety": dict(DEFAULT_TAIL_RISK_SAFETY),
    }
