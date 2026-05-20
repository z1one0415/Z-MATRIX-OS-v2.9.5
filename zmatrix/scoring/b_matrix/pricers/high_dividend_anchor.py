from __future__ import annotations
from .base_pricer import BaseBMatrixPricer, clamp
from ..contracts import BMatrixInput, BaseType, TrapFlag
from ..shareholder_return_analyzer import shareholder_return_score, fcf_dividend_coverage_score
from ..valuation_context import valuation_score_by_type


class HighDividendAnchorPricer(BaseBMatrixPricer):
    base_type = BaseType.HIGH_DIVIDEND_ANCHOR

    def weighted_score(self, stock: BMatrixInput):
        traps: list[TrapFlag] = []
        valuation, val_traps, val_flags = valuation_score_by_type(stock, self.base_type)
        traps.extend(val_traps)
        shareholder = shareholder_return_score(stock)
        fcf_cov = fcf_dividend_coverage_score(stock)
        debt = 5.0 if stock.debt_ratio is None else clamp(10.0 - max(stock.debt_ratio - 0.4, 0) * 10)
        policy = stock.policy_stability_score if stock.policy_stability_score is not None else (7.0 if stock.is_state_owned else 5.0)
        score = shareholder * 0.30 + fcf_cov * 0.25 + debt * 0.20 + policy * 0.15 + valuation * 0.10
        q_flags = []
        if fcf_cov < 5:
            q_flags.append("fcf_dividend_coverage_warning")
        return score, traps, val_flags, q_flags, ["SHAREHOLDER_RETURN_ANCHOR"]
