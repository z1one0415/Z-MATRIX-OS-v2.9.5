"""LIMIT_DOWN_BLACKHOLE — isolate when mass limit-down or locked ticker"""
from __future__ import annotations
import hashlib

from zmatrix.tail_risk.schemas import DEFAULT_TAIL_RISK_SAFETY


def evaluate_limit_down_blackhole(*, market_signals: dict, ticker_context: dict | None = None) -> dict:
    """If limit_down >= 80 or ticker is locked, return ISOLATE."""
    ldn = market_signals.get("limit_down_count", 0)
    tc = ticker_context or {}
    locked = tc.get("limit_down_locked", False) or tc.get("open_escape_failed", False)
    triggered = ldn >= 80 or locked

    if not triggered:
        return {
            "gate_id": "0" * 32, "gate_type": "LIMIT_DOWN_BLACKHOLE",
            "state": "NORMAL", "decision": "ALLOW", "action_downgrade": "NO_ACTION",
            "reason": "no trigger", "evidence": {"limit_down_count": ldn, "locked": locked},
            "affected_roles": [], "affected_tickers": [],
            "freeze_new_entries": False, "allow_existing_position_review": True,
            "requires_human_review": False, "safety": dict(DEFAULT_TAIL_RISK_SAFETY),
        }

    seed = f"LIMIT_DOWN_BLACKHOLE|{ldn}|{locked}"
    gid = hashlib.sha256(seed.encode()).hexdigest()[:32]
    return {
        "gate_id": gid, "gate_type": "LIMIT_DOWN_BLACKHOLE",
        "state": "CRASH", "decision": "ISOLATE",
        "action_downgrade": "RISK_ISOLATE",
        "reason": f"limit_down={ldn} locked={locked}",
        "evidence": {"limit_down_count": ldn, "limit_down_locked": locked},
        "affected_roles": ["C_SHORT_EVENT", "D_BLACK_HORSE"],
        "affected_tickers": [],
        "freeze_new_entries": True, "allow_existing_position_review": True,
        "requires_human_review": True, "safety": dict(DEFAULT_TAIL_RISK_SAFETY),
    }
