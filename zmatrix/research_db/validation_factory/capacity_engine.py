"""F4: Capacity Engine — validate factor capacity at 1M/10M/100M/500M/1B."""
from __future__ import annotations
from dataclasses import dataclass, field

CAPACITY_LEVELS = [1_000_000, 10_000_000, 100_000_000, 500_000_000, 1_000_000_000]

@dataclass
class CapacityResult:
    factor_id: str; level: float; ic_at_capacity: float = 0.0
    turnover_at_capacity: float = 0.0; slippage_estimate: float = 0.0
    feasible: bool = True; max_capacity: float = 0.0
    production_allowed: bool = field(default=False, repr=False)
    def __post_init__(self): self.production_allowed=False

class CapacityEngine:
    @staticmethod
    def estimate_slippage(aum: float, daily_volume: float, participation_rate: float = 0.05) -> float:
        if daily_volume <= 0: return 1.0
        trade_size = aum * participation_rate / 250
        return (trade_size / daily_volume) * 100  # Impact in bps

    @staticmethod
    def evaluate_capacity(factor_id: str, ic_series: list[float], daily_volume: float, aum: float) -> CapacityResult:
        r = CapacityResult(factor_id=factor_id, level=aum)
        r.ic_at_capacity = sum(ic_series)/len(ic_series) if ic_series else 0.0
        r.slippage_estimate = CapacityEngine.estimate_slippage(aum, daily_volume)
        r.feasible = r.slippage_estimate < 0.50 and abs(r.ic_at_capacity) > 0.01
        r.max_capacity = daily_volume * 250 * 0.05 / 20
        return r

    @staticmethod
    def evaluate_all_levels(factor_id: str, ic_series: list[float], daily_volume: float) -> list[CapacityResult]:
        return [CapacityEngine.evaluate_capacity(factor_id, ic_series, daily_volume, aum) for aum in CAPACITY_LEVELS]
