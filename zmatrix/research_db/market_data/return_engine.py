"""Phase 3-C: Return Engine — gross return, annualized, holding days."""
from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional

class CalculationStatus(str, Enum):
    READY="READY"; MISSING_ENTRY="MISSING_ENTRY"; MISSING_EXIT="MISSING_EXIT"
    INVALID_PRICE="INVALID_PRICE"; INSUFFICIENT_HORIZON="INSUFFICIENT_HORIZON"; UNKNOWN="UNKNOWN"

@dataclass
class ReturnResult:
    entry_price: float; exit_price: float; gross_return: float = 0.0
    annualized_return: float = 0.0; holding_days: int = 0
    calculation_status: str = "UNKNOWN"; production_allowed: bool = field(default=False,repr=False)
    def __post_init__(self): self.production_allowed=False

class ReturnEngine:
    @staticmethod
    def compute_gross_return(entry_price: float, exit_price: float) -> float:
        if entry_price <= 0: return 0.0
        return (exit_price - entry_price) / entry_price

    @staticmethod
    def compute_annualized_return(gross_return: float, holding_days: int) -> float:
        if holding_days <= 0: return 0.0
        return ((1 + gross_return) ** (365 / holding_days)) - 1

    @staticmethod
    def calculate_holding_days(entry_date: str, exit_date: str, calendar) -> int:
        d = entry_date; count = 0
        while d and d < exit_date:
            d = calendar.next_trade_day(d)
            count += 1
        return count

    @staticmethod
    def compute_return(entry_price: float, exit_price: float, entry_date: str,
                       exit_date: str, calendar, horizon_engine=None) -> ReturnResult:
        r = ReturnResult(entry_price=entry_price, exit_price=exit_price)
        if entry_price <= 0 or exit_price <= 0:
            r.calculation_status = CalculationStatus.INVALID_PRICE.value; return r
        r.gross_return = ReturnEngine.compute_gross_return(entry_price, exit_price)
        r.holding_days = ReturnEngine.calculate_holding_days(entry_date, exit_date, calendar)
        r.annualized_return = ReturnEngine.compute_annualized_return(r.gross_return, r.holding_days)
        r.calculation_status = CalculationStatus.READY.value
        return r
