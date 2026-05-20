from __future__ import annotations
from .contracts import BMatrixInput, BMatrixResult, BaseType, BRating, BEligibility
from .base_type_classifier import classify_base_type
from .pricers.high_dividend_anchor import HighDividendAnchorPricer
from .pricers.compounding_quality import CompoundingQualityPricer
from .pricers.resource_cash_cow import ResourceCashCowPricer
from .pricers.state_infra_monopoly import StateInfraMonopolyPricer
from .pricers.brand_scarcity_monopoly import BrandScarcityMonopolyPricer


_PRICERS = {
    BaseType.HIGH_DIVIDEND_ANCHOR: HighDividendAnchorPricer(),
    BaseType.COMPOUNDING_QUALITY: CompoundingQualityPricer(),
    BaseType.RESOURCE_CASH_COW: ResourceCashCowPricer(),
    BaseType.STATE_INFRA_MONOPOLY: StateInfraMonopolyPricer(),
    BaseType.BRAND_SCARCITY_MONOPOLY: BrandScarcityMonopolyPricer(),
}


def evaluate_b_matrix(stock: BMatrixInput) -> BMatrixResult:
    base_type = classify_base_type(stock)
    if base_type == BaseType.NOT_B_MATRIX:
        return BMatrixResult(
            symbol=stock.symbol,
            name=stock.name,
            matrix="B_MATRIX",
            base_type=base_type,
            score_raw=0.0,
            score_final=0.0,
            rating=BRating.D,
            rating_cap=BRating.D,
            eligibility=BEligibility.B_DISQUALIFIED,
            trap_flags=["NOT_B_MATRIX"],
            next_trigger=["not eligible for bottom-holding role"],
        )
    result = _PRICERS[base_type].score(stock)
    result.validate_no_trade_action()
    return result
