"""Batch-A: Cost Attribution — decompose return drag by cost type."""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional

@dataclass
class CostBreakdown:
    ticker: str; signal_date: str
    gross_return: float = 0.0
    commission_drag: float = 0.0
    stamp_duty_drag: float = 0.0
    slippage_drag: float = 0.0
    execution_drag: float = 0.0
    total_cost_drag: float = 0.0
    net_return: float = 0.0
    cost_erosion_pct: float = 0.0
    production_allowed: bool = field(default=False, repr=False)
    def __post_init__(self): self.production_allowed = False

class CostAttribution:
    @staticmethod
    def attribute_costs(ticker: str, signal_date: str, gross_return: float,
                         entry_amount: float, sell_amount: float,
                         commission_bps: float = 3.0, stamp_bps: float = 5.0,
                         slippage_bps: float = 10.0) -> CostBreakdown:
        cd = CostBreakdown(ticker=ticker, signal_date=signal_date, gross_return=gross_return)
        if entry_amount <= 0: return cd
        cd.commission_drag = (entry_amount * (commission_bps / 10000) + sell_amount * (commission_bps / 10000)) / entry_amount
        cd.stamp_duty_drag = (sell_amount * (stamp_bps / 10000)) / entry_amount
        cd.slippage_drag = ((entry_amount + sell_amount) * (slippage_bps / 10000)) / entry_amount
        cd.execution_drag = 0.0  # Reserved
        cd.total_cost_drag = cd.commission_drag + cd.stamp_duty_drag + cd.slippage_drag + cd.execution_drag
        cd.net_return = gross_return - cd.total_cost_drag
        cd.cost_erosion_pct = (cd.total_cost_drag / abs(gross_return)) * 100 if gross_return != 0 else 0.0
        return cd

    @staticmethod
    def batch_attribute(records: list[dict]) -> list[CostBreakdown]:
        return [CostAttribution.attribute_costs(**r) for r in records]
