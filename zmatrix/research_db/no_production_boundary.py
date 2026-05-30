"""ResearchDB No Production Boundary — hard safety gate enforcement."""
from __future__ import annotations

SAFETY_FLAGS = {
    "real_trade_allowed": False,
    "broker_order_allowed": False,
    "runtime_enabled": False,
    "auto_buy_allowed": False,
    "auto_sell_allowed": False,
    "production_allowed": False,
    "paper_only": True,
    "human_review_required": True,
}


def check_boundary() -> dict:
    """Return current safety boundary status. All flags must remain False/BLOCKED."""
    return {
        "status": "SAFE",
        "flags": dict(SAFETY_FLAGS),
        "production_allowed": SAFETY_FLAGS["production_allowed"],
        "broker_allowed": SAFETY_FLAGS["broker_order_allowed"],
        "real_trade_allowed": SAFETY_FLAGS["real_trade_allowed"],
    }


def is_production_allowed() -> bool:
    """Always returns False. Hard-gated."""
    return False
