"""Batch-I: Portfolio Liquidity — stress scenario simulation."""
from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional


class LiquidityEventType(str, Enum):
    LIMIT_DOWN = "LIMIT_DOWN"
    CONSECUTIVE_LIMIT_DOWN = "CONSECUTIVE_LIMIT_DOWN"
    SUSPEND = "SUSPEND"
    ILLIQUID = "ILLIQUID"


@dataclass
class LiquidityEvent:
    event_id: str
    ticker: str
    event_type: str
    start_date: str
    days: int = 1
    impact_pct: float = 0.0
    production_allowed: bool = field(default=False, repr=False)

    def __post_init__(self):
        self.production_allowed = False


@dataclass
class LiquidityResult:
    portfolio_id: str
    total_impact_pct: float = 0.0
    fillable_pct: float = 100.0
    blocked_tickers: int = 0
    event_details: dict = field(default_factory=dict)
    production_allowed: bool = field(default=False, repr=False)

    def __post_init__(self):
        self.production_allowed = False


class PortfolioLiquidity:
    EVENT_FILL_RATES = {
        LiquidityEventType.LIMIT_DOWN.value: 0.60,
        LiquidityEventType.CONSECUTIVE_LIMIT_DOWN.value: 0.30,
        LiquidityEventType.SUSPEND.value: 0.0,
        LiquidityEventType.ILLIQUID.value: 0.10,
    }

    EVENT_IMPACT = {
        LiquidityEventType.LIMIT_DOWN.value: 5.0,
        LiquidityEventType.CONSECUTIVE_LIMIT_DOWN.value: 15.0,
        LiquidityEventType.SUSPEND.value: 20.0,
        LiquidityEventType.ILLIQUID.value: 8.0,
    }

    @staticmethod
    def simulate_liquidity_shock(
        portfolio: dict,
        events: list[LiquidityEvent],
    ) -> LiquidityResult:
        portfolio_id = portfolio.get("portfolio_id", "UNKNOWN")
        tickers = portfolio.get("tickers", [])
        event_lookup = {e.ticker: e for e in events}
        total_impact = 0.0
        blocked = 0
        ticker_count = max(len(tickers), 1)
        for ticker in tickers:
            event = event_lookup.get(ticker)
            if event is None:
                continue
            blocked += 1
            total_impact += PortfolioLiquidity.EVENT_IMPACT.get(
                event.event_type, 5.0
            )
        impact_pct = total_impact / ticker_count
        fillable = 1.0
        for ticker in tickers:
            event = event_lookup.get(ticker)
            if event is None:
                continue
            fill_rate = PortfolioLiquidity.EVENT_FILL_RATES.get(
                event.event_type, 0.60
            )
            fillable *= fill_rate ** (1.0 / ticker_count)
        return LiquidityResult(
            portfolio_id=portfolio_id,
            total_impact_pct=round(impact_pct, 2),
            fillable_pct=round(fillable * 100.0, 2),
            blocked_tickers=blocked,
            event_details={"event_count": len(events)},
        )

    @staticmethod
    def compute_fillability(
        portfolio: dict,
        events: list[LiquidityEvent],
    ) -> LiquidityResult:
        return PortfolioLiquidity.simulate_liquidity_shock(portfolio, events)
