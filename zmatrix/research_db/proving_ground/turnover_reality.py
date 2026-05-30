"""F.5-4: Turnover Reality Test — high/low turnover, small/mid/large cap, high/low vol."""
from __future__ import annotations
from dataclasses import dataclass, field

@dataclass
class TurnoverRealityResult:
    factor_id: str; daily_turnover: float = 0.0; annual_turnover: float = 0.0
    small_cap_turnover: float = 0.0; mid_cap_turnover: float = 0.0; large_cap_turnover: float = 0.0
    high_vol_turnover: float = 0.0; low_vol_turnover: float = 0.0
    estimated_cost_bps_annual: float = 0.0; capacity_grade: str = ""
    feasible: bool = True
    production_allowed: bool = field(default=False, repr=False)
    def __post_init__(self): self.production_allowed=False

class TurnoverReality:
    @staticmethod
    def compute_turnover(holdings: list[set], period_days: int = 1) -> float:
        if len(holdings) < 2: return 0.0
        changes = sum(len(h1 - h2) + len(h2 - h1) for h1, h2 in zip(holdings, holdings[1:]))
        return (changes / len(holdings[0]) / (len(holdings) - 1)) if holdings[0] and len(holdings) > 1 else 0.0

    @staticmethod
    def analyze(factor_id: str, holdings_history: dict, slippage_bps: float = 10.0) -> TurnoverRealityResult:
        r = TurnoverRealityResult(factor_id=factor_id)
        def _to(l): return TurnoverReality.compute_turnover(list(map(set, l)), len(l))
        r.daily_turnover = _to(holdings_history.get("all", [[]]))
        r.small_cap_turnover = _to(holdings_history.get("small_cap", [[]]))
        r.mid_cap_turnover = _to(holdings_history.get("mid_cap", [[]]))
        r.large_cap_turnover = _to(holdings_history.get("large_cap", [[]]))
        r.high_vol_turnover = _to(holdings_history.get("high_vol", [[]]))
        r.low_vol_turnover = _to(holdings_history.get("low_vol", [[]]))
        r.annual_turnover = r.daily_turnover * 250
        r.estimated_cost_bps_annual = r.annual_turnover * slippage_bps
        r.capacity_grade = "A" if r.annual_turnover < 12 else "B" if r.annual_turnover < 25 else "C" if r.annual_turnover < 50 else "D" if r.annual_turnover < 100 else "E"
        r.feasible = r.capacity_grade in ("A","B","C")
        return r
