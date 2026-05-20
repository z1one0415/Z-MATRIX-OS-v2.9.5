from dataclasses import dataclass
from typing import List

@dataclass
class WeeklyCycleResult:
    cycle_count: int
    avg_elasticity: float
    passed: bool
    reason: str


def simple_weekly_cycles(weekly_prices: List[float], min_elasticity: float = 0.25) -> WeeklyCycleResult:
    """Simple causal-safe historical cycle quality approximation.

    It uses sign changes on smoothed weekly returns, not for real-time entry.
    """
    if len(weekly_prices) < 52:
        return WeeklyCycleResult(0, 0.0, False, "insufficient weekly history")
    # crude swing detection by local extrema in historical window
    peaks = []
    valleys = []
    for i in range(2, len(weekly_prices)-2):
        p = weekly_prices[i]
        if p > weekly_prices[i-1] and p > weekly_prices[i+1] and p > weekly_prices[i-2] and p > weekly_prices[i+2]:
            peaks.append((i,p))
        if p < weekly_prices[i-1] and p < weekly_prices[i+1] and p < weekly_prices[i-2] and p < weekly_prices[i+2]:
            valleys.append((i,p))
    cycles = []
    for vi, vp in valleys:
        future_peaks = [(pi, pp) for pi, pp in peaks if pi > vi]
        if not future_peaks:
            continue
        pi, pp = future_peaks[0]
        if vp > 0:
            e = (pp - vp) / vp
            if e >= min_elasticity:
                cycles.append(e)
    count = len(cycles)
    avg = sum(cycles)/count if count else 0.0
    passed = 2 <= count <= 5 and avg >= min_elasticity
    return WeeklyCycleResult(count, avg, passed, "ok" if passed else "cycle count or elasticity not enough")
