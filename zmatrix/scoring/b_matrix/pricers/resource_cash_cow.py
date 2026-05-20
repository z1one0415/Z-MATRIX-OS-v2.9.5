from __future__ import annotations
from .base_pricer import BaseBMatrixPricer, clamp
from ..contracts import BMatrixInput, BaseType, TrapFlag
from ..shareholder_return_analyzer import shareholder_return_score
from ..valuation_context import valuation_score_by_type


class ResourceCashCowPricer(BaseBMatrixPricer):
    base_type = BaseType.RESOURCE_CASH_COW

    def weighted_score(self, stock: BMatrixInput):
        traps: list[TrapFlag] = []
        valuation, val_traps, val_flags = valuation_score_by_type(stock, self.base_type)
        traps.extend(val_traps)
        cost = stock.cost_curve_score if stock.cost_curve_score is not None else 5.0
        resource = stock.resource_quality_score if stock.resource_quality_score is not None else 5.0
        cycle_norm = 6.0
        if stock.profit_percentile_5y is not None:
            cycle_norm = clamp(8.0 - max(stock.profit_percentile_5y - 0.5, 0) * 8.0)
        shareholder = shareholder_return_score(stock)
        balance = 5.0 if stock.debt_ratio is None else clamp(10.0 - max(stock.debt_ratio - 0.45, 0) * 10)
        score = cost * 0.25 + resource * 0.20 + cycle_norm * 0.20 + shareholder * 0.15 + balance * 0.10 + valuation * 0.10
        return score, traps, val_flags, [], ["CYCLE_NORMALIZED_CASH_COW"]
