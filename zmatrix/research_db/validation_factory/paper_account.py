"""F1-A: Paper Account — simulated trading account."""
from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, timezone

@dataclass
class PaperPosition:
    ticker: str; quantity: int = 0; avg_price: float = 0.0
    market_price: float = 0.0; unrealized_pnl: float = 0.0; realized_pnl: float = 0.0
    production_allowed: bool = field(default=False, repr=False)
    def __post_init__(self): self.production_allowed=False

@dataclass
class PaperAccount:
    account_id: str; initial_capital: float = 1000000.0
    cash: float = 1000000.0; total_equity: float = 1000000.0
    positions: dict = field(default_factory=dict)  # ticker → PaperPosition
    nav_history: list = field(default_factory=list)
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    production_allowed: bool = field(default=False, repr=False)
    def __post_init__(self): self.production_allowed=False

    def update_market_prices(self, prices: dict):
        for ticker, price in prices.items():
            if ticker in self.positions:
                self.positions[ticker].market_price = price
                self.positions[ticker].unrealized_pnl = (price - self.positions[ticker].avg_price) * self.positions[ticker].quantity

    def compute_equity(self) -> float:
        mv = sum(p.market_price * p.quantity for p in self.positions.values())
        self.total_equity = self.cash + mv; return self.total_equity

    def record_nav(self, date: str):
        self.compute_equity(); self.nav_history.append({"date": date, "equity": self.total_equity, "cash": self.cash})
