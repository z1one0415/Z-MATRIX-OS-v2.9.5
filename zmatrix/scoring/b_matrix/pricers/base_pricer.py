from __future__ import annotations
from abc import ABC, abstractmethod
from ..contracts import BMatrixInput, BMatrixResult, BaseType, BRating
from ..quality_trap_detector import QualityTrapDetector
from ..rating_cap_engine import cap_from_traps, apply_rating_cap, rating_from_score, eligibility_from_rating
from ..thesis_snapshot import build_thesis_snapshot


def clamp(x: float, lo: float = 0.0, hi: float = 10.0) -> float:
    return max(lo, min(hi, x))


def score_stability_roe(roe_5y: float | None) -> float:
    # Corrected v2.1 formula: ROE 8% -> 5, ROE 20% -> 10.
    if roe_5y is None:
        return 5.0
    return clamp(5.0 + (roe_5y - 8.0) / 12.0 * 5.0)


class BaseBMatrixPricer(ABC):
    base_type: BaseType

    def __init__(self) -> None:
        self.quality_detector = QualityTrapDetector()

    @abstractmethod
    def weighted_score(self, stock: BMatrixInput) -> tuple[float, list, list[str], list[str], list[str]]:
        """Return score, additional traps, valuation flags, quality flags, secondary traits."""

    def score(self, stock: BMatrixInput) -> BMatrixResult:
        quality_traps = self.quality_detector.detect(stock)
        score, traps2, valuation_flags, quality_flags, secondary_traits = self.weighted_score(stock)
        traps = quality_traps + traps2
        cap = cap_from_traps(traps)
        raw_rating = rating_from_score(score)
        final_rating = apply_rating_cap(raw_rating, cap)
        eligibility = eligibility_from_rating(final_rating, bool(traps))
        snapshot = build_thesis_snapshot(stock, self.base_type)
        score_cap_value = {BRating.A: 10.0, BRating.B: 7.99, BRating.C: 6.49, BRating.D: 4.99}[cap]
        result = BMatrixResult(
            symbol=stock.symbol,
            name=stock.name,
            matrix="B_MATRIX",
            base_type=self.base_type,
            score_raw=round(score, 2),
            score_final=round(min(score, score_cap_value), 2),
            rating=final_rating,
            rating_cap=cap,
            eligibility=eligibility,
            quality_flags=quality_flags,
            valuation_flags=valuation_flags,
            trap_flags=[t.code for t in traps],
            secondary_traits=secondary_traits,
            thesis_snapshot_required=True,
            thesis_stop=snapshot.thesis_stop_rules,
            next_trigger=["valuation enters safety zone", "R-Matrix gives accumulation window", "L3 sector stabilizes"],
        )
        result.validate_no_trade_action()
        return result
