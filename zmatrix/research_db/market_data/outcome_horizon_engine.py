"""Phase 3-B: Outcome Horizon Engine — strict T20/T60 forward-day validation."""
from __future__ import annotations
from typing import Optional
from zmatrix.research_db.market_data.outcome_schema import (
    OutcomeHorizon, OutcomeHorizonResult, OutcomeReadinessStatus, HORIZON_FORWARD_DAYS,
)
from zmatrix.research_db.market_data.trading_calendar import TradingCalendar
from zmatrix.research_db.market_data.price_bar_store import PriceBarStore


class OutcomeHorizonEngine:
    def __init__(self, calendar: TradingCalendar, bar_store: PriceBarStore):
        self.calendar = calendar
        self.bar_store = bar_store

    def resolve_exit_date(self, observation_date: str, horizon: str) -> Optional[str]:
        if horizon not in HORIZON_FORWARD_DAYS: return None
        n = HORIZON_FORWARD_DAYS[horizon]
        return self.calendar.forward_trade_day(observation_date, n)

    def evaluate_horizon(self, ticker: str, observation_date: str, horizon: str) -> OutcomeHorizonResult:
        result = OutcomeHorizonResult(ticker=ticker, observation_date=observation_date, horizon=horizon,
                                       required_forward_days=HORIZON_FORWARD_DAYS.get(horizon, 0))
        # 1. Validate horizon
        if horizon not in HORIZON_FORWARD_DAYS:
            result.readiness_status = OutcomeReadinessStatus.INVALID_HORIZON.value
            result.reason = f"Unknown horizon: {horizon}"; return result
        n = HORIZON_FORWARD_DAYS[horizon]

        # 2. Check forward days
        if not self.calendar.has_forward_days(observation_date, n):
            result.readiness_status = OutcomeReadinessStatus.INSUFFICIENT_FORWARD_DAYS.value
            result.reason = f"Need {n} forward days, insufficient from {observation_date}"; return result

        exit_date = self.calendar.forward_trade_day(observation_date, n)
        result.exit_date = exit_date

        # 3. Entry bar
        entry_bar = self.bar_store.get_bar(ticker, observation_date)
        if entry_bar is None:
            result.readiness_status = OutcomeReadinessStatus.MISSING_ENTRY_BAR.value
            result.reason = f"No entry bar for {ticker} on {observation_date}"; return result
        result.entry_bar_available = True
        result.entry_suspended = self.bar_store.detect_suspension(ticker, observation_date)
        if result.entry_suspended:
            result.readiness_status = OutcomeReadinessStatus.SUSPENDED_ENTRY.value
            result.reason = f"{ticker} suspended on entry {observation_date}"; return result

        # 4. Exit bar
        exit_bar = self.bar_store.get_bar(ticker, exit_date)
        if exit_bar is None:
            result.readiness_status = OutcomeReadinessStatus.MISSING_EXIT_BAR.value
            result.reason = f"No exit bar for {ticker} on {exit_date}"; return result
        result.exit_bar_available = True
        result.exit_suspended = self.bar_store.detect_suspension(ticker, exit_date)
        if result.exit_suspended:
            result.readiness_status = OutcomeReadinessStatus.SUSPENDED_EXIT.value
            result.reason = f"{ticker} suspended on exit {exit_date}"; return result

        # 5. READY
        result.readiness_status = OutcomeReadinessStatus.READY.value
        result.reason = ""; return result

    def evaluate_many(self, requests: list[dict]) -> list[OutcomeHorizonResult]:
        return [self.evaluate_horizon(r["ticker"], r["observation_date"], r["horizon"]) for r in requests]
