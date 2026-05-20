from dataclasses import dataclass
from typing import List, Optional
import math

@dataclass
class RollingTrendPoint:
    index: int
    alpha: float
    beta: float
    trend: float
    residual: float
    lookahead_safe: bool = True


def _ols(y: List[float]) -> tuple[float, float]:
    """Simple OLS y = alpha + beta*x for x=0..n-1."""
    n = len(y)
    if n < 2:
        raise ValueError("OLS requires at least 2 points")
    xs = list(range(n))
    x_bar = (n - 1) / 2
    y_bar = sum(y) / n
    denom = sum((x - x_bar) ** 2 for x in xs)
    if denom == 0:
        return y_bar, 0.0
    beta = sum((x - x_bar) * (v - y_bar) for x, v in zip(xs, y)) / denom
    alpha = y_bar - beta * x_bar
    return alpha, beta


def rolling_ols_residuals(prices: List[float], window: int = 250, include_current_for_next_day: bool = False) -> List[RollingTrendPoint]:
    """Compute rolling OLS trend and residuals without lookahead.

    If include_current_for_next_day=False, point t is evaluated using data [t-window, t),
    suitable for intraday/today decisions.
    If True, point t uses [t-window+1, t+1] and must only be used for t+1 decisions.
    """
    if window < 20:
        raise ValueError("window too short for trend channel")
    logp = [math.log(p) for p in prices if p and p > 0]
    if len(logp) != len(prices):
        raise ValueError("prices must be positive")
    out: List[RollingTrendPoint] = []
    start = window if not include_current_for_next_day else window - 1
    for t in range(start, len(logp)):
        if include_current_for_next_day:
            train = logp[t - window + 1:t + 1]
            x_eval = window - 1
        else:
            train = logp[t - window:t]
            x_eval = window
        if len(train) < window:
            continue
        alpha, beta = _ols(train)
        trend = alpha + beta * x_eval
        residual = logp[t] - trend
        out.append(RollingTrendPoint(index=t, alpha=alpha, beta=beta, trend=trend, residual=residual, lookahead_safe=True))
    return out


def latest_rising_channel_signal(prices: List[float], window: int = 250) -> Optional[RollingTrendPoint]:
    pts = rolling_ols_residuals(prices, window=window, include_current_for_next_day=False)
    return pts[-1] if pts else None
