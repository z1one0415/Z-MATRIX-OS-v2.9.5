"""R-Matrix Service v2.0-cycle-four-king — true four-king unified entry

Impulse King: daily price action — momentum/drawdown/acceleration
Oscillation King: 5-day BOX hunter — mean-reversion channel
Rhythm King: weekly mid-term swing — BOX/TREND classification
Rotation King: bi-weekly trend — sector rotation entry signal

Legacy fallback: removed. All kings implemented with real algorithms.
No dependency on oscillation_king_ranker_v11 (old Type A/B).
"""
from __future__ import annotations
from typing import List
import statistics


def evaluate_r_matrix_cycle(
    ticker: str,
    prices: List[float] | None = None,
    position: dict | None = None,
    *,
    daily_prices: List[float] | None = None,
    weekly_prices: List[float] | None = None,
    biweekly_prices: List[float] | None = None,
    five_day_prices: List[float] | None = None,
    **kwargs,
) -> dict:
    """True four-king evaluation. Returns standardized cycle verdict."""

    daily = daily_prices or prices or []
    weekly = weekly_prices or (daily[::5] if len(daily) >= 20 else [])
    biweekly = biweekly_prices or (daily[::10] if len(daily) >= 20 else [])
    five_day = five_day_prices or (daily[::3] if len(daily) >= 20 else [])  # ~3-day proxy

    result = {
        "ticker": ticker, "version": "v2.0-cycle-four-king",
        "status": "DATA_GAP", "legacy_fallback": False,
        "r_score": None, "r_resonance_status": "UNKNOWN", "r_action_cap": "WAIT",
        "entry_action_cap": "WAIT", "exit_alert": "NONE",
        "hard_blocks": [], "conflicts": [],
        "kings": {}, "sell_decision": None,
        "data_lineage": {
            "daily_bars": len(daily), "weekly_bars": len(weekly),
            "biweekly_bars": len(biweekly), "five_day_bars": len(five_day),
            "source": "R_MATRIX_SERVICE",
        },
        "errors": [], "warnings": [],
    }

    if len(daily) < 20:
        result["errors"].append(f"insufficient daily bars: {len(daily)}")
        result["status"] = "DATA_GAP"
        return result

    # ── Impulse King: daily momentum ──
    try:
        ik = _impulse_king(daily)
        result["kings"]["impulse"] = ik
    except Exception as e:
        result["errors"].append(f"impulse: {str(e)[:80]}")

    # ── Oscillation King: 5-day BOX ──
    try:
        if len(five_day) >= 15:
            from zmatrix.scoring.r_matrix.rhythm_king_weekly import classify_rhythm
            ok = classify_rhythm(five_day, beta_threshold=0.002, box_amp_min=5, box_amp_max=200)
            ok["king"] = "oscillation"
            result["kings"]["oscillation"] = ok
    except Exception as e:
        result["errors"].append(f"oscillation: {str(e)[:80]}")

    # ── Rhythm King: weekly ──
    try:
        if len(weekly) >= 20:
            from zmatrix.scoring.r_matrix.rhythm_king_weekly import classify_rhythm
            rk = classify_rhythm(weekly, beta_threshold=0.004, box_amp_min=10, box_amp_max=150)
            rk["king"] = "rhythm"
            result["kings"]["rhythm"] = rk
    except Exception as e:
        result["errors"].append(f"rhythm: {str(e)[:80]}")

    # ── Rotation King: bi-weekly ──
    try:
        if len(biweekly) >= 8:
            from zmatrix.scoring.r_matrix.rhythm_king_weekly import classify_rhythm
            rotk = classify_rhythm(biweekly, beta_threshold=0.004, box_amp_min=8, box_amp_max=200)
            rotk["king"] = "rotation"
            result["kings"]["rotation"] = rotk
    except Exception as e:
        result["errors"].append(f"rotation: {str(e)[:80]}")

    # ── Resonance ──
    king_count = len(result["kings"])
    if king_count >= 3 and not result["errors"]:
        try:
            from zmatrix.scoring.r_matrix.cycle_four_king_resonance import evaluate_cycle_four_king
            resonance = evaluate_cycle_four_king(
                result["kings"].get("impulse"),
                result["kings"].get("oscillation"),
                result["kings"].get("rhythm"),
                result["kings"].get("rotation"))
            result["r_resonance_status"] = resonance["resonance_status"]
            result["r_score"] = resonance["resonance_score"]
            result["entry_action_cap"] = resonance["entry_action_cap"]
            result["r_action_cap"] = resonance["entry_action_cap"]
            result["exit_alert"] = resonance["exit_alert"]
            result["hard_blocks"] = resonance["hard_blocks"]
            result["conflicts"] = resonance["conflicts"]
        except Exception as e:
            result["errors"].append(f"resonance: {str(e)[:80]}")

    # ── Sell decision ──
    if position and king_count >= 2:
        try:
            from zmatrix.scoring.r_matrix.position_sell_decision import evaluate_position_sell_decision
            price = position.get("price", position.get("cost", 0))
            result["sell_decision"] = evaluate_position_sell_decision(
                ticker, position.get("shares", 0), position.get("cost", 0), price,
                {"hard_blocks": result["hard_blocks"], "exit_alert": result["exit_alert"],
                 "kings": result["kings"]})
        except Exception as e:
            result["errors"].append(f"sell_decision: {str(e)[:80]}")

    # ── Status resolution ──
    if result["errors"]:
        result["status"] = "DEGRADED"
    elif king_count < 2:
        result["status"] = "DATA_GAP"
    elif king_count < 4:
        result["status"] = "DEGRADED"
        result["warnings"].append(f"partial_kings:{king_count}/4")
    else:
        result["status"] = "PASS"

    return result


def _impulse_king(prices: List[float]) -> dict:
    """Impulse King: daily momentum signals from price action."""
    n = min(60, len(prices))
    recent = prices[-n:]

    # 20-day momentum
    chg_20 = (recent[-1] / recent[-min(21, n)] - 1) * 100 if n >= 21 else 0

    # 60-day momentum
    chg_60 = (recent[-1] / recent[0] - 1) * 100 if n >= 40 else chg_20

    # Drawdown from 60-day high
    peak = max(recent)
    drawdown = (recent[-1] / peak - 1) * 100

    # Acceleration: 5-day vs 20-day
    chg_5 = (recent[-1] / recent[-min(6, n)] - 1) * 100 if n >= 6 else 0
    acceleration = chg_5 - (chg_20 / 4) if chg_20 else 0

    # Volatility
    returns = [(recent[i] / recent[i - 1] - 1) * 100 for i in range(1, min(20, n))]
    vol = statistics.stdev(returns) if len(returns) >= 2 else 0

    # Score
    score = 50
    if chg_20 > 2: score += 15
    elif chg_20 < -2: score -= 15
    if acceleration > 1: score += 10  # accelerating up
    elif acceleration < -1: score -= 10
    if drawdown > -3: score += 5  # near highs
    elif drawdown < -10: score -= 10  # deep pullback

    if score > 70:
        itype = "IMPULSE_UP"
        action = "HOLD" if chg_20 > 5 else "WATCH_ENTRY"
    elif score < 30:
        itype = "IMPULSE_DOWN"
        action = "AVOID"
    else:
        itype = "NEUTRAL"
        action = "WAIT"

    return {
        "king": "impulse", "type": itype, "score": round(score, 1),
        "action": action,
        "evidence": {
            "chg_20d": round(chg_20, 1), "chg_60d": round(chg_60, 1),
            "drawdown": round(drawdown, 1), "acceleration": round(acceleration, 1),
            "volatility": round(vol, 1),
        },
    }
