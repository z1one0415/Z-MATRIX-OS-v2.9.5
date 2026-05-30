"""F.5-3: Capacity Calibration — ADV%, Participation%, Order Book Depth → A/B/C/D/E grades."""
from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum

class CapacityGrade(str, Enum):
    A="A"; B="B"; C="C"; D="D"; E="E"

@dataclass
class CapacityCalibrationResult:
    factor_id: str; aum: float; adv_pct: float = 0.0; participation_pct: float = 0.0
    order_book_depth_impact: float = 0.0; grade: str = "E"; feasible: bool = False
    production_allowed: bool = field(default=False, repr=False)
    def __post_init__(self): self.production_allowed=False

class CapacityCalibration:
    CAPACITY_LEVELS = [1e6, 5e6, 10e6, 50e6, 100e6, 500e6, 1e9]
    @staticmethod
    def calibrate(factor_id: str, aum: float, daily_volume: float, order_book_depth: float = 0.0) -> CapacityCalibrationResult:
        r = CapacityCalibrationResult(factor_id=factor_id, aum=aum)
        adv = aum * 0.05 / 250
        r.adv_pct = adv / daily_volume if daily_volume > 0 else 1.0
        r.participation_pct = adv / daily_volume * 2 if daily_volume > 0 else 1.0
        r.order_book_depth_impact = adv / order_book_depth if order_book_depth > 0 else 1.0
        total_impact = r.adv_pct + r.participation_pct * 0.5 + r.order_book_depth_impact * 0.5
        r.grade = ("A" if total_impact < 0.01 else "B" if total_impact < 0.05 else
                   "C" if total_impact < 0.10 else "D" if total_impact < 0.20 else "E")
        r.feasible = r.grade in ("A","B","C")
        return r

    @staticmethod
    def calibrate_all_levels(factor_id: str, daily_volume: float, order_book_depth: float = 0.0) -> list[CapacityCalibrationResult]:
        return [CapacityCalibration.calibrate(factor_id, lv, daily_volume, order_book_depth) for lv in CapacityCalibration.CAPACITY_LEVELS]
