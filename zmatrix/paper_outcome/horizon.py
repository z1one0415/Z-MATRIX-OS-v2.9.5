"""Trading Day Horizon — anchor paper dates to trading days"""
from __future__ import annotations
from datetime import datetime, timedelta

_WEEKEND = {5, 6}  # Sat=5, Sun=6

def anchor_to_next_trading_day(date_str: str) -> str:
    """If date falls on weekend, shift to next Monday."""
    dt = datetime.strptime(date_str, "%Y-%m-%d")
    while dt.weekday() in _WEEKEND:
        dt += timedelta(days=1)
    return dt.strftime("%Y-%m-%d")

def trading_day_offset(base_date: str, offset: int) -> str:
    """Add `offset` trading days to base_date."""
    dt = datetime.strptime(base_date, "%Y-%m-%d")
    count = 0
    while count < offset:
        dt += timedelta(days=1)
        if dt.weekday() not in _WEEKEND:
            count += 1
    return dt.strftime("%Y-%m-%d")

def build_horizon_dates(entry_date: str) -> dict:
    """Return T+5/T+20/T+60 as trading-day-anchored dates."""
    anchored = anchor_to_next_trading_day(entry_date)
    return {
        "entry_date": anchored,
        "t5_date": trading_day_offset(anchored, 5),
        "t20_date": trading_day_offset(anchored, 20),
        "t60_date": trading_day_offset(anchored, 60),
    }
