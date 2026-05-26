"""Return Calculator — compute T5/T20/T60 returns from price path"""
from __future__ import annotations


def calc_actual_return(entry_price: float, price_path: list[float],
                       horizon_days: int) -> float | None:
    """Calculate actual return for a given horizon."""
    if not price_path or entry_price <= 0:
        return None
    idx = min(horizon_days, len(price_path)) - 1
    if idx < 0:
        return None
    return round((price_path[idx] - entry_price) / entry_price * 100, 2)


def calc_all_horizons(entry_price: float, price_path: list[float]) -> dict:
    """Calculate T5/T20/T60 returns. Returns None for missing data."""
    return {
        "actual_return_t5": calc_actual_return(entry_price, price_path, 5),
        "actual_return_t20": calc_actual_return(entry_price, price_path, 20),
        "actual_return_t60": calc_actual_return(entry_price, price_path, 60),
    }
