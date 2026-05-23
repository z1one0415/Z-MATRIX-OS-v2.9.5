"""R-Matrix Service v2.0 — unified entry point for four-king cycle evaluation.

G09, G14, and any pipeline needing cycle analysis must call this service.
Do not call oscillation_king_ranker or rhythm_king_weekly directly from pipelines.
"""
from __future__ import annotations
from typing import List


def evaluate_r_matrix_cycle(
    ticker: str,
    daily_prices: List[float] | None = None,
    weekly_prices: List[float] | None = None,
    biweekly_prices: List[float] | None = None,
    five_day_prices: List[float] | None = None,
    position: dict | None = None,
) -> dict:
    """Run full four-king cycle evaluation for a ticker.

    Returns dict with impulse/oscillation/rhythm/rotation + resonance + sell_decision.
    """
    result = {"ticker": ticker, "kings": {}, "available": False}

    try:
        from zmatrix.scoring.r_matrix.oscillation_king_ranker_v11 import (
            rank_type_a_horizontal, rank_type_b_rising_channel)
        
        # Impulse king (daily)
        if daily_prices and len(daily_prices) >= 260:
            a = rank_type_a_horizontal(ticker, "", daily_prices)
            b = rank_type_b_rising_channel(ticker, "", daily_prices)
            best = a if a.score >= b.score else b
            result["kings"]["impulse"] = {
                "type": best.oscillation_type, "score": best.score,
                "action": best.allowed_action,
            }
    except Exception:
        pass

    try:
        from zmatrix.scoring.r_matrix.rhythm_king_weekly import classify_rhythm
        from zmatrix.scoring.r_matrix.cycle_four_king_resonance import evaluate_cycle_four_king
        from zmatrix.scoring.r_matrix.position_sell_decision import evaluate_position_sell_decision

        # Oscillation king (5-day)
        if five_day_prices and len(five_day_prices) >= 20:
            result["kings"]["oscillation"] = classify_rhythm(
                five_day_prices, beta_threshold=0.002, box_amp_min=5, box_amp_max=200)

        # Rhythm king (weekly)
        if weekly_prices and len(weekly_prices) >= 20:
            result["kings"]["rhythm"] = classify_rhythm(
                weekly_prices, beta_threshold=0.004, box_amp_min=10, box_amp_max=150)

        # Rotation king (biweekly)
        if biweekly_prices and len(biweekly_prices) >= 6:
            result["kings"]["rotation"] = classify_rhythm(
                biweekly_prices, beta_threshold=0.004, box_amp_min=8, box_amp_max=200)

        # Resonance
        resonance = evaluate_cycle_four_king(
            result["kings"].get("impulse"),
            result["kings"].get("oscillation"),
            result["kings"].get("rhythm"),
            result["kings"].get("rotation"))
        result["resonance"] = resonance

        # Sell decision
        if position:
            price = position.get("price", position.get("cost", 0))
            result["sell_decision"] = evaluate_position_sell_decision(
                ticker=ticker, shares=position.get("shares", 0),
                cost=position.get("cost", 0), current_price=price,
                resonance=resonance)

        result["available"] = bool(result["kings"])
    except Exception:
        pass

    return result
