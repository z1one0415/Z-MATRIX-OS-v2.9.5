"""Drawdown Calculator — entry-relative max adverse excursion + peak-to-trough"""
from __future__ import annotations


def calc_max_drawdown(price_path: list[float]) -> float | None:
    """Calculate max drawdown % from peak (peak-to-trough)."""
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


def calc_entry_relative_drawdown(entry_price: float, price_path: list[float]) -> dict:
    """Calculate max adverse excursion relative to ENTRY price.
    
    Returns dict with:
    - max_adverse_excursion_pct: largest % below entry (negative = loss)
    - max_gain_before_loss_pct: largest gain before any subsequent loss
    - is_fake_winner: True if had >5% gain then ended < entry
    """
    if not price_path or entry_price <= 0:
        return {"max_adverse_excursion_pct": None, "max_gain_before_loss_pct": None,
                "is_fake_winner": False}
    min_price = min(price_path)
    max_price = max(price_path)
    mae = round((min_price - entry_price) / entry_price * 100, 2)  # negative = loss
    mgb = round((max_price - entry_price) / entry_price * 100, 2)
    # Fake winner: had >5% gain but ended below entry
    last_price = price_path[-1]
    is_fake = mgb > 5 and last_price < entry_price
    return {
        "max_adverse_excursion_pct": mae,
        "max_gain_before_loss_pct": mgb,
        "is_fake_winner": is_fake,
    }


def calc_all_drawdowns(price_path: list[float]) -> dict:
    return {
        "max_drawdown_t20": calc_max_drawdown(price_path[:20]) if len(price_path) >= 20 else None,
        "max_drawdown_t60": calc_max_drawdown(price_path[:60]) if len(price_path) >= 60 else None,
    }
