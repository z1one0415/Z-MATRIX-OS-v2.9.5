"""ResearchDB Outcome Horizon Policy — strict T20/T60 enforcement."""
from __future__ import annotations

HORIZON_DAYS = {
    "T1": 1,
    "T3": 3,
    "T5": 5,
    "T10": 10,
    "T20": 20,
    "T60": 60,
}


def validate_forward_window(horizon: str, available_forward_days: int) -> dict:
    """Validate whether sufficient forward trading days exist for the horizon.

    Args:
        horizon: One of T1, T3, T5, T10, T20, T60.
        available_forward_days: Number of forward trading days available.

    Returns:
        dict with ready, blocked_reason, required_days, available_days.
    """
    if horizon not in HORIZON_DAYS:
        return {
            "horizon": horizon,
            "required_days": 0,
            "available_days": available_forward_days,
            "ready": False,
            "blocked_reason": f"UNKNOWN_HORIZON_{horizon}",
            "fallback_last_price_allowed": False,
        }

    required_days = HORIZON_DAYS[horizon]
    if available_forward_days >= required_days:
        return {
            "horizon": horizon,
            "required_days": required_days,
            "available_days": available_forward_days,
            "ready": True,
            "blocked_reason": None,
            "fallback_last_price_allowed": False,
        }

    return {
        "horizon": horizon,
        "required_days": required_days,
        "available_days": available_forward_days,
        "ready": False,
        "blocked_reason": "INSUFFICIENT_FORWARD_TRADING_DAYS",
        "fallback_last_price_allowed": False,
    }
