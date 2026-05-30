"""Phase 3-B: Alpha Calculator — compute returns and alpha vs benchmarks."""
from __future__ import annotations
from typing import Optional


def compute_gross_return(entry_price: float, exit_price: float) -> float:
    return (exit_price - entry_price) / entry_price


def compute_benchmark_return(
    benchmark_prices: dict[str, float],
    entry_date: str,
    exit_date: str,
) -> Optional[float]:
    entry = benchmark_prices.get(entry_date)
    exit_ = benchmark_prices.get(exit_date)
    if entry is None or exit_ is None:
        return None
    return (exit_ - entry) / entry


def compute_alpha(
    signal_return: float,
    benchmark_return: Optional[float],
) -> Optional[float]:
    if benchmark_return is None:
        return None
    return signal_return - benchmark_return


def compute_max_excursion(
    bars: list[dict],
    entry_price: float,
) -> tuple[float, float]:
    max_fav = 0.0
    max_adv = 0.0
    closest_to_entry = entry_price
    for bar in bars:
        high = bar.get("high", bar.get("close", entry_price))
        low = bar.get("low", bar.get("close", entry_price))
        fav = (high - entry_price) / entry_price
        adv = (entry_price - low) / entry_price
        if fav > max_fav:
            max_fav = fav
        if adv > max_adv:
            max_adv = adv
    return round(max_fav, 10), round(max_adv, 10)
