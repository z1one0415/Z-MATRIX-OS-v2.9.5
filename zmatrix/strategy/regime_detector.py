"""Regime Detector v1.0 — detects market regime from price series.

States: REVERSAL, MOMENTUM, TRANSITION, DATA_INSUFFICIENT, HIGH_VOL_NOISE.
"""
def detect_reversal_momentum_regime(price_series: list[float]) -> dict:
    """Detect regime from closing price series. Returns regime dict with metrics."""
    if not price_series or len(price_series) < 20:
        return _result("DATA_INSUFFICIENT", price_series)

    daily_returns = [(price_series[i] / max(price_series[i-1], 0.0001) - 1)
                     for i in range(1, len(price_series))]

    # Up-day-next-down probability
    up_days = sum(1 for r in daily_returns if r > 0)
    if up_days < 5:
        return _result("DATA_INSUFFICIENT", price_series)

    up_day_next_down = 0
    for i in range(len(daily_returns) - 1):
        if daily_returns[i] > 0 and daily_returns[i+1] < 0:
            up_day_next_down += 1
    prob = up_day_next_down / max(up_days - 1, 1)

    # Avg up-run length
    runs = []
    current = 0
    for r in daily_returns:
        if r > 0:
            current += 1
        else:
            if current > 0:
                runs.append(current)
            current = 0
    if current > 0:
        runs.append(current)
    avg_run = sum(runs) / max(len(runs), 1)
    max_run = max(runs) if runs else 0
    run_ge_3 = sum(1 for r in runs if r >= 3) / max(len(runs), 1)

    # Trend slope 20d
    n = min(20, len(price_series))
    slope = (price_series[-1] - price_series[-n]) / max(price_series[-n], 0.0001) / n if len(price_series) >= 2 else 0

    # Volatility
    rets_20 = daily_returns[-20:] if len(daily_returns) >= 20 else daily_returns
    if rets_20:
        m = sum(rets_20) / len(rets_20)
        vol = (sum((r - m)**2 for r in rets_20) / len(rets_20))**0.5
    else:
        vol = 0

    # Regime determination
    if prob >= 0.52:
        regime = "REVERSAL"
    elif prob <= 0.47 and avg_run >= 2.1:
        regime = "MOMENTUM"
    elif 0.48 <= prob <= 0.51:
        regime = "TRANSITION"
    else:
        regime = "TRANSITION"  # default when not clearly in one camp

    # Override: high volatility with direction uncertainty → noise
    if vol > 0.04 and avg_run < 1.5:
        regime = "HIGH_VOL_NOISE"

    return _result(regime, price_series, prob, avg_run, max_run, run_ge_3, slope, vol)

def _result(regime, prices, prob=None, avg_run=None, max_run=None, run_ge_3=None, slope=None, vol=None):
    return {
        "regime_state": regime,
        "up_day_next_down_probability": round(prob, 4) if prob is not None else None,
        "avg_up_run_length": round(avg_run, 2) if avg_run is not None else None,
        "max_up_run_length": max_run,
        "run_ge_3_ratio": round(run_ge_3, 4) if run_ge_3 is not None else None,
        "trend_slope_20d": round(slope, 6) if slope is not None else None,
        "volatility_20d": round(vol, 6) if vol is not None else None,
        "valid_observations": len(prices) if prices else 0,
        "confidence": "MEDIUM",
        "alpha_claim_allowed": False,
    }
