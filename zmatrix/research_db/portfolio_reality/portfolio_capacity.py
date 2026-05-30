"""Batch-I: Portfolio Capacity — capacity analysis at multiple AUM levels."""
from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional

AUM_LEVELS = [100_000_000, 500_000_000, 1_000_000_000, 5_000_000_000, 10_000_000_000]


class CapacityGrade(str, Enum):
    A = "A"; B = "B"; C = "C"; D = "D"; E = "E"


@dataclass
class CapacityResult:
    portfolio_id: str
    aum: float
    adv_pct: float = 0.0
    impact_bps: float = 0.0
    feasible: bool = False
    grade: str = CapacityGrade.E.value
    details: dict = field(default_factory=dict)
    production_allowed: bool = field(default=False, repr=False)

    def __post_init__(self):
        self.production_allowed = False


class PortfolioCapacity:
    GRADE_THRESHOLDS = {
        CapacityGrade.A: (0.0, 2.0),
        CapacityGrade.B: (2.0, 5.0),
        CapacityGrade.C: (5.0, 10.0),
        CapacityGrade.D: (10.0, 20.0),
        CapacityGrade.E: (20.0, float("inf")),
    }

    @staticmethod
    def _assign_grade(adv_pct: float) -> str:
        for grade, (lo, hi) in PortfolioCapacity.GRADE_THRESHOLDS.items():
            if lo <= adv_pct < hi:
                return grade.value
        return CapacityGrade.E.value

    @staticmethod
    def analyze_capacity(
        portfolio: dict,
        aum: float,
        daily_volume: float,
    ) -> CapacityResult:
        portfolio_id = portfolio.get("portfolio_id", "UNKNOWN")
        if daily_volume <= 0:
            return CapacityResult(
                portfolio_id=portfolio_id, aum=aum,
                adv_pct=float("inf"), impact_bps=0.0,
                feasible=False, grade=CapacityGrade.E.value,
            )
        adv_pct = (aum / daily_volume) * 100.0
        impact_bps = adv_pct * 0.25
        feasible = adv_pct <= 30.0
        grade = PortfolioCapacity._assign_grade(adv_pct)
        return CapacityResult(
            portfolio_id=portfolio_id, aum=aum,
            adv_pct=round(adv_pct, 2), impact_bps=round(impact_bps, 2),
            feasible=feasible, grade=grade,
            details={"ticker_count": len(portfolio.get("tickers", [])),
                      "daily_volume": daily_volume},
        )

    @staticmethod
    def analyze_all_levels(
        portfolio: dict,
        daily_volume: float,
    ) -> list[CapacityResult]:
        return [
            PortfolioCapacity.analyze_capacity(portfolio, aum, daily_volume)
            for aum in AUM_LEVELS
        ]
