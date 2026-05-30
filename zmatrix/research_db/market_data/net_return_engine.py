"""Phase 3-C: Net Return Engine — gross minus total cost."""
from __future__ import annotations
from dataclasses import dataclass, field

@dataclass
class NetReturnResult:
    gross_return: float = 0.0; commission_cost: float = 0.0
    stamp_duty_cost: float = 0.0; slippage_cost: float = 0.0
    total_cost: float = 0.0; net_return: float = 0.0
    production_allowed: bool = field(default=False,repr=False)
    def __post_init__(self): self.production_allowed=False
    def __post_init_verify__(self):
        """Verify: net_return == gross_return - total_cost"""
        expected = self.gross_return - self.total_cost
        assert abs(self.net_return - expected) < 1e-10,             f"net_return {self.net_return} != gross {self.gross_return} - total {self.total_cost}"

class NetReturnEngine:
    @staticmethod
    def compute_net_return(gross_return: float, total_cost: float, entry_amount: float) -> float:
        if entry_amount <= 0: return 0.0
        return gross_return - (total_cost / entry_amount)

    @staticmethod
    def compute_full_net_result(entry_price: float, exit_price: float, entry_amount: float,
                                 commission_bps: float = 3.0, stamp_bps: float = 5.0,
                                 slippage_bps: float = 10.0) -> NetReturnResult:
        from .trading_cost_engine import TradingCostEngine
        gross = (exit_price - entry_price) / entry_price if entry_price > 0 else 0.0
        buy_amt = entry_amount; sell_amt = entry_amount * (1 + gross)
        cost = TradingCostEngine.compute_total_cost(buy_amt, sell_amt, commission_bps, stamp_bps, slippage_bps)
        total = cost.total_cost
        net = gross - (total / entry_amount) if entry_amount > 0 else 0.0
        return NetReturnResult(gross_return=gross, commission_cost=cost.buy_commission + cost.sell_commission,
                               stamp_duty_cost=cost.stamp_duty, slippage_cost=cost.slippage,
                               total_cost=total, net_return=net)
