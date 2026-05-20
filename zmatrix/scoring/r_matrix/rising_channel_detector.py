from dataclasses import dataclass
from typing import List
from .rolling_trend_channel import rolling_ols_residuals

@dataclass
class RisingChannelResult:
    passed: bool
    beta: float
    residuals: list[float]
    reason: str


def detect_rising_channel(prices: List[float], window: int = 250, min_beta: float = 0.00005, max_beta: float = 0.01) -> RisingChannelResult:
    pts = rolling_ols_residuals(prices, window=window, include_current_for_next_day=False)
    if len(pts) < 30:
        return RisingChannelResult(False, 0.0, [], "insufficient rolling trend points")
    beta = pts[-1].beta
    residuals = [p.residual for p in pts]
    if beta <= min_beta:
        return RisingChannelResult(False, beta, residuals, "trend slope not positive enough")
    if beta > max_beta:
        return RisingChannelResult(False, beta, residuals, "trend slope too steep; possible mania")
    return RisingChannelResult(True, beta, residuals, "rising channel candidate")
