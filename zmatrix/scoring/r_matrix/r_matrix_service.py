"""R-Matrix Service v2.0-cycle-four-king — shared entry for G09/G14."""
from __future__ import annotations
from typing import List


def evaluate_r_matrix_cycle(ticker: str, prices: List[float] | None = None,
                            position: dict | None = None, **kwargs) -> dict:
    """Run four-king cycle evaluation. Returns standardized dict."""
    result = {
        "ticker": ticker, "version": "v2.0-cycle-four-king",
        "status": "DATA_GAP", "r_score": None,
        "r_resonance_status": "UNKNOWN", "r_action_cap": "WAIT",
        "kings": {}, "sell_decision": None, "errors": [], "warnings": [],
    }

    if not prices or len(prices) < 60:
        result["errors"].append(f"insufficient data: {len(prices or [])} bars")
        return result

    try:
        from zmatrix.scoring.r_matrix.rhythm_king_weekly import classify_rhythm, rhythm_king_weekly
        from zmatrix.scoring.r_matrix.cycle_four_king_resonance import evaluate_cycle_four_king
        from zmatrix.scoring.r_matrix.position_sell_decision import evaluate_position_sell_decision

        # Impulse (daily) — fallback to old Type A/B for now
        try:
            from zmatrix.scoring.r_matrix.oscillation_king_ranker_v11 import rank_type_a_horizontal, rank_type_b_rising_channel
            a = rank_type_a_horizontal(ticker, "", prices)
            b = rank_type_b_rising_channel(ticker, "", prices)
            best = a if a.score >= b.score else b
            result["kings"]["impulse"] = {"type": best.oscillation_type, "score": best.score, "action": best.allowed_action}
        except Exception as e:
            result["errors"].append(f"impulse: {str(e)[:80]}")

        # Rhythm (weekly) — sample every 5th bar
        weekly = prices[::5]
        if len(weekly) >= 20:
            result["kings"]["rhythm"] = rhythm_king_weekly(weekly)
        else:
            result["errors"].append(f"weekly insufficient: {len(weekly)} bars")

        # Oscillation (5-day proxy) — sample every bar
        if len(prices) >= 100:
            sampled = prices[::2][:50]
            if len(sampled) >= 20:
                result["kings"]["oscillation"] = classify_rhythm(sampled, beta_threshold=0.002, box_amp_min=5, box_amp_max=200)

        # Resonance if enough kings
        if len(result["kings"]) >= 2:
            resonance = evaluate_cycle_four_king(
                result["kings"].get("impulse"),
                result["kings"].get("oscillation"),
                result["kings"].get("rhythm"),
                result["kings"].get("rotation"))
            result["r_resonance_status"] = resonance["resonance_status"]
            result["r_score"] = resonance["resonance_score"]
            result["r_action_cap"] = resonance["entry_action_cap"]
            result["status"] = "PASS"

            if position:
                price = position.get("price", position.get("cost", 0))
                result["sell_decision"] = evaluate_position_sell_decision(
                    ticker, position.get("shares", 0), position.get("cost", 0), price, resonance)
    except Exception as e:
        result["status"] = "ERROR"
        result["errors"].append(str(e)[:120])

    if not result["errors"]:
        result["status"] = result["status"] or "PASS"
    elif not result["kings"]:
        result["status"] = "DATA_GAP"

    return result
