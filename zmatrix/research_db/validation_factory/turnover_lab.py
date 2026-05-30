"""F5: Turnover Lab — turnover / slippage / capacity interaction."""
from __future__ import annotations
from dataclasses import dataclass, field

@dataclass
class TurnoverResult:
    factor_id: str; daily_turnover: float = 0.0; annual_turnover: float = 0.0
    slippage_annual_bps: float = 0.0; cost_erosion_annual: float = 0.0
    capacity_constrained: bool = False
    production_allowed: bool = field(default=False, repr=False)
    def __post_init__(self): self.production_allowed=False

class TurnoverLab:
    @staticmethod
    def compute_turnover(positions: list[dict]) -> float:
        if len(positions) < 2: return 0.0
        changes = 0; prev = set(p["ticker"] for p in positions[0].get("tickers",[]))
        for p in positions[1:]:
            cur = set(p.get("tickers",[]))
            changes += len(prev - cur) + len(cur - prev)
            prev = cur
        return changes / (len(positions) - 1) if len(positions) > 1 else 0.0

    @staticmethod
    def estimate_annual_cost(turnover: float, slippage_bps: float = 10.0) -> float:
        return turnover * slippage_bps * 250 / 10000

    @staticmethod
    def analyze(factor_id: str, positions: list[dict], slippage_bps: float = 10.0, capacity_aum: float = 0.0) -> TurnoverResult:
        r = TurnoverResult(factor_id=factor_id)
        r.daily_turnover = TurnoverLab.compute_turnover(positions)
        r.annual_turnover = r.daily_turnover * 250
        r.slippage_annual_bps = r.annual_turnover * slippage_bps
        r.cost_erosion_annual = TurnoverLab.estimate_annual_cost(r.daily_turnover, slippage_bps)
        r.capacity_constrained = r.annual_turnover > 100 and capacity_aum > 100_000_000
        return r
