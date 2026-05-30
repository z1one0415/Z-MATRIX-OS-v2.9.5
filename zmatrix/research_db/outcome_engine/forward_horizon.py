"""Phase 3-B: Outcome Horizon Engine — strict T20/T60 forward-day enforcement."""
from __future__ import annotations
from typing import Optional

from zmatrix.research_db.market_data.trading_calendar import TradingCalendar

HORIZON_DAYS = {
    "T1": 1,
    "T3": 3,
    "T5": 5,
    "T10": 10,
    "T20": 20,
    "T60": 60,
}


class OutcomeHorizonEngine:
    def __init__(self, calendar: TradingCalendar):
        self._calendar = calendar

    def compute_horizon(self, signal_date: str, horizon: str) -> dict:
        required_days = HORIZON_DAYS.get(horizon)

        if required_days is None:
            return {
                "horizon": horizon,
                "ready": False,
                "blocked_reason": f"UNKNOWN_HORIZON_{horizon}",
                "required_days": 0,
                "available_days": 0,
                "fallback_last_price_allowed": False,
            }

        available_days = 0
        d = signal_date
        while self._calendar.forward_trade_day(signal_date, available_days + 1) is not None:
            available_days += 1

        if available_days >= required_days:
            return {
                "horizon": horizon,
                "ready": True,
                "blocked_reason": None,
                "required_days": required_days,
                "available_days": available_days,
                "fallback_last_price_allowed": False,
            }

        return {
            "horizon": horizon,
            "ready": False,
            "blocked_reason": "INSUFFICIENT_FORWARD_TRADING_DAYS",
            "required_days": required_days,
            "available_days": available_days,
            "fallback_last_price_allowed": False,
        }

    def compute_all_horizons(self, signal_date: str) -> dict[str, dict]:
        return {h: self.compute_horizon(signal_date, h) for h in HORIZON_DAYS}
