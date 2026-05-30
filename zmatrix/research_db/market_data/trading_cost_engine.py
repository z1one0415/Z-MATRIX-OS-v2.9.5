"""Phase 3-C: Trading Cost Engine — commission, stamp duty, slippage."""
from __future__ import annotations
from dataclasses import dataclass, field

@dataclass
class CostResult:
    buy_commission: float = 0.0; sell_commission: float = 0.0
    stamp_duty: float = 0.0; slippage: float = 0.0
    total_cost: float = 0.0
    production_allowed: bool = field(default=False,repr=False)
    def __post_init__(self): self.production_allowed=False

class TradingCostEngine:
    @staticmethod
    def compute_buy_commission(amount: float, commission_bps: float = 3.0) -> float:
        """Commission in bps (basis points). Default 3bp = 0.0003."""
        return amount * (commission_bps / 10000)

    @staticmethod
    def compute_sell_commission(amount: float, commission_bps: float = 3.0) -> float:
        return amount * (commission_bps / 10000)

    @staticmethod
    def compute_stamp_duty(sell_amount: float, stamp_bps: float = 5.0) -> float:
        """Stamp duty on sell only. Default 5bp."""
        return sell_amount * (stamp_bps / 10000)

    @staticmethod
    def compute_slippage(amount: float, slippage_bps: float = 10.0) -> float:
        return amount * (slippage_bps / 10000)

    @staticmethod
    def compute_total_cost(buy_amount: float = 0.0, sell_amount: float = 0.0,
                            commission_bps: float = 3.0, stamp_bps: float = 5.0,
                            slippage_bps: float = 10.0) -> CostResult:
        bc = TradingCostEngine.compute_buy_commission(buy_amount, commission_bps)
        sc = TradingCostEngine.compute_sell_commission(sell_amount, commission_bps)
        sd = TradingCostEngine.compute_stamp_duty(sell_amount, stamp_bps)
        sl = TradingCostEngine.compute_slippage(buy_amount + sell_amount, slippage_bps)
        return CostResult(buy_commission=bc, sell_commission=sc, stamp_duty=sd, slippage=sl,
                          total_cost=bc + sc + sd + sl)

    @staticmethod
    def market_impact_cost(amount: float) -> float:
        """Reserved. Always returns 0.0 for Phase 3-C."""
        return 0.0
