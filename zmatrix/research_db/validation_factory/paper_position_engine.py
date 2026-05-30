"""F1-D: Paper Position Engine — position tracking."""
from __future__ import annotations
from dataclasses import dataclass, field

@dataclass
class PositionSnapshot:
    date: str; positions: dict = field(default_factory=dict); total_mv: float = 0.0
    cash: float = 0.0; equity: float = 0.0; exposure: float = 0.0
    production_allowed: bool = field(default=False, repr=False)
    def __post_init__(self): self.production_allowed=False

class PaperPositionEngine:
    @staticmethod
    def snapshot(date: str, account) -> PositionSnapshot:
        equity = account.compute_equity()
        s = PositionSnapshot(date=date, positions={t: {"qty":p.quantity,"price":p.market_price,"pnl":p.unrealized_pnl}
                           for t,p in account.positions.items()}, cash=account.cash, equity=equity,
                           total_mv=equity-account.cash, exposure=(equity-account.cash)/equity if equity>0 else 0)
        return s
