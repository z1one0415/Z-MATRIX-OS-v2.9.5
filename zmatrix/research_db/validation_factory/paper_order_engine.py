"""F1-B: Paper Order Engine — order types and validation."""
from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum

class OrderSide(str, Enum): BUY="BUY"; SELL="SELL"
class OrderType(str, Enum): MARKET="MARKET"; LIMIT="LIMIT"

@dataclass
class PaperOrder:
    order_id: str; ticker: str; side: str; order_type: str
    quantity: int; price: float = 0.0; status: str = "PENDING"
    filled_qty: int = 0; filled_price: float = 0.0
    production_allowed: bool = field(default=False, repr=False)
    def __post_init__(self): self.production_allowed=False

class PaperOrderEngine:
    def __init__(self, account: "PaperAccount"): self.account = account
    def create_order(self, order_id: str, ticker: str, side: str, qty: int, price: float = 0.0, order_type: str = "MARKET") -> PaperOrder:
        return PaperOrder(order_id=order_id, ticker=ticker, side=side, order_type=order_type, quantity=qty, price=price)
    def validate_order(self, order: PaperOrder) -> bool:
        if order.side == OrderSide.BUY.value and order.price * order.quantity > self.account.cash: return False
        if order.side == OrderSide.SELL.value:
            pos = self.account.positions.get(order.ticker)
            if not pos or pos.quantity < order.quantity: return False
        return True
