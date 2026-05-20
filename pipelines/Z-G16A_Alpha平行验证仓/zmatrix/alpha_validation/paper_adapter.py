from __future__ import annotations

from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from typing import Any, Dict
from uuid import uuid4


@dataclass
class PaperFill:
    paper_trade_id: str
    symbol: str
    side: str
    quantity: int
    fill_price: float
    fee: float
    slippage: float
    filled_at: str
    world: str = "PAPER_WORLD"

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class SimplePaperExecutionAdapter:
    """Small deterministic paper fill adapter.

    This is intentionally not a broker connector. It estimates a paper fill under
    provided price/slippage assumptions and returns PAPER_WORLD fill records.
    """

    def __init__(self, fee_rate: float = 0.0003, slippage_bps: float = 5.0):
        self.fee_rate = fee_rate
        self.slippage_bps = slippage_bps

    def open_fill(self, symbol: str, quantity: int, reference_price: float, side: str = "BUY") -> PaperFill:
        if quantity <= 0:
            raise ValueError("quantity must be positive")
        if reference_price <= 0:
            raise ValueError("reference_price must be positive")
        if side not in {"BUY", "SELL"}:
            raise ValueError("side must be BUY or SELL")
        sign = 1 if side == "BUY" else -1
        slippage = reference_price * self.slippage_bps / 10000.0 * sign
        fill_price = reference_price + slippage
        notional = abs(fill_price * quantity)
        fee = notional * self.fee_rate
        return PaperFill(
            paper_trade_id=f"pt_{uuid4().hex[:16]}",
            symbol=symbol,
            side=side,
            quantity=quantity,
            fill_price=round(fill_price, 4),
            fee=round(fee, 4),
            slippage=round(slippage, 4),
            filled_at=datetime.now(timezone.utc).isoformat(),
        )
