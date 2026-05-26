"""DOMESTIC_LIQUIDITY_CRASH — freeze when liquidity scissors or index drawdown"""
from __future__ import annotations
import hashlib

from zmatrix.tail_risk.schemas import DEFAULT_TAIL_RISK_SAFETY


def evaluate_domestic_liquidity_crash(*, market_signals: dict) -> dict:
    ls = market_signals.get("liquidity_scissor", 0.0)
    scs = market_signals.get("small_cap_liquidity_score", 0.0)
    dbs = market_signals.get("derivative_basis_stress", 0.0)
    dd5 = market_signals.get("index_drawdown_5d", 0.0)

    triggered = (ls >= 0.50 and scs <= 0.25) or dbs >= 0.75 or dd5 <= -0.05

    if not triggered:
        return {
            "gate_id": "0"*32, "gate_type": "DOMESTIC_LIQUIDITY_CRASH",
            "state": "NORMAL", "decision": "ALLOW", "action_downgrade": "NO_ACTION",
            "reason": "no trigger", "evidence": {},
            "affected_roles": [], "affected_tickers": [],
            "freeze_new_entries": False, "allow_existing_position_review": True,
            "requires_human_review": False, "safety": dict(DEFAULT_TAIL_RISK_SAFETY),
        }

    seed = f"DOMESTIC_LIQUIDITY_CRASH|{ls}|{dbs}"
    gid = hashlib.sha256(seed.encode()).hexdigest()[:32]
    return {
        "gate_id": gid, "gate_type": "DOMESTIC_LIQUIDITY_CRASH",
        "state": "CRASH", "decision": "FREEZE",
        "action_downgrade": "REVIEW_TO_FREEZE",
        "reason": f"liquidity_scissor={ls:.2f} stress={dbs:.2f} dd={dd5:.2f}",
        "evidence": {"liquidity_scissor": ls, "small_cap_score": scs, "basis_stress": dbs, "drawdown_5d": dd5},
        "affected_roles": ["D_BLACK_HORSE", "C_SHORT_EVENT"],
        "affected_tickers": [],
        "freeze_new_entries": True, "allow_existing_position_review": True,
        "requires_human_review": True, "safety": dict(DEFAULT_TAIL_RISK_SAFETY),
    }
