from __future__ import annotations
from .base_pricer import BaseBMatrixPricer
from ..contracts import BMatrixInput, BaseType, TrapFlag
from ..shareholder_return_analyzer import shareholder_return_score
from ..valuation_context import valuation_score_by_type


class StateInfraMonopolyPricer(BaseBMatrixPricer):
    base_type = BaseType.STATE_INFRA_MONOPOLY

    def weighted_score(self, stock: BMatrixInput):
        traps: list[TrapFlag] = []
        valuation, val_traps, val_flags = valuation_score_by_type(stock, self.base_type)
        traps.extend(val_traps)
        policy = stock.policy_stability_score if stock.policy_stability_score is not None else 7.0
        cashflow_visibility = 5.0
        if stock.ocf_3y and stock.net_profit_3y and sum(stock.net_profit_3y) > 0:
            cashflow_visibility = min(10.0, 4.0 + (sum(stock.ocf_3y) / sum(stock.net_profit_3y)) * 3.0)
        monopoly = stock.asset_monopoly_score if stock.asset_monopoly_score is not None else (7.0 if stock.is_state_owned else 5.0)
        dividend = shareholder_return_score(stock)
        score = policy * 0.25 + cashflow_visibility * 0.25 + monopoly * 0.20 + dividend * 0.15 + valuation * 0.15
        return score, traps, val_flags, [], ["POLICY_ASSET_MONOPOLY"]
