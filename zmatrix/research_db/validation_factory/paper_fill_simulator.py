"""F1-C: Paper Fill Simulator — simulated order execution."""
from __future__ import annotations
from .paper_account import PaperPosition
from dataclasses import dataclass, field

@dataclass
class FillResult:
    order_id: str; filled: bool = False; fill_price: float = 0.0; fill_qty: int = 0
    slippage_bps: float = 0.0; status: str = "UNFILLED"
    production_allowed: bool = field(default=False, repr=False)
    def __post_init__(self): self.production_allowed=False

class PaperFillSimulator:
    @staticmethod
    def simulate_fill(order, market_prices: dict, slippage_bps: float = 10.0) -> FillResult:
        mp = market_prices.get(order.ticker, 0)
        if mp <= 0: return FillResult(order_id=order.order_id, status="NO_PRICE")
        fill_price = mp * (1 + (slippage_bps / 10000) * (1 if order.side == "BUY" else -1))
        r = FillResult(order_id=order.order_id, filled=True, fill_price=fill_price, fill_qty=order.quantity, slippage_bps=slippage_bps, status="FILLED")
        return r

    @staticmethod
    def execute(order, account, market_prices: dict, slippage_bps: float = 10.0) -> FillResult:
        fill = PaperFillSimulator.simulate_fill(order, market_prices, slippage_bps)
        if not fill.filled: return fill
        cost = fill.fill_price * fill.fill_qty
        if order.side == "BUY":
            if cost > account.cash: return FillResult(order_id=order.order_id, status="INSUFFICIENT_CASH")
            account.cash -= cost
            pos = account.positions.get(order.ticker, PaperPosition(ticker=order.ticker))
            if order.ticker not in account.positions: account.positions[order.ticker] = pos
            new_total_cost = pos.avg_price * pos.quantity + fill.fill_price * fill.fill_qty
            pos.quantity += fill.fill_qty
            pos.avg_price = new_total_cost / pos.quantity if pos.quantity > 0 else 0
        else:
            pos = account.positions.get(order.ticker)
            if not pos or pos.quantity < fill.fill_qty: return FillResult(order_id=order.order_id, status="INSUFFICIENT_POSITION")
            account.cash += cost
            pos.realized_pnl += (fill.fill_price - pos.avg_price) * fill.fill_qty
            pos.quantity -= fill.fill_qty
            if pos.quantity == 0: del account.positions[order.ticker]
        return fill
