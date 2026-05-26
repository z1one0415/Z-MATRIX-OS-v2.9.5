"""Drawdown Calculator — compute max drawdown from price path"""
from __future__ import annotations


def calc_max_drawdown(price_path: list[float]) -> float | None:
    """Calculate max drawdown % from peak."""
    if not price_path or len(price_path) < 2:
        return None
    peak = price_path[0]
    max_dd = 0.0
    for p in price_path:
        if p > peak:
            peak = p
        dd = (peak - p) / peak * 100
        if dd > max_dd:
            max_dd = dd
    return round(max_dd, 2)


def calc_all_drawdowns(price_path: list[float]) -> dict:
    """Calculate max drawdown for T5/T20/T60 windows."""
    return {
        "max_drawdown_t20": calc_max_drawdown(price_path[:20]) if len(price_path) >= 20 else None,
        "max_drawdown_t60": calc_max_drawdown(price_path[:60]) if len(price_path) >= 60 else None,
    }
