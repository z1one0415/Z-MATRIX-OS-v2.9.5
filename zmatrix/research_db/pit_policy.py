"""ResearchDB PIT Safety Policy — Point-in-Time validation."""
from __future__ import annotations
from enum import Enum


class PITStatus(str, Enum):
    PIT_SAFE = "PIT_SAFE"
    PIT_UNSAFE = "PIT_UNSAFE"
    CURRENT_SNAPSHOT_ONLY = "CURRENT_SNAPSHOT_ONLY"
    UNKNOWN_PIT_STATUS = "UNKNOWN_PIT_STATUS"
    BLOCKED_FOR_BACKTEST = "BLOCKED_FOR_BACKTEST"


def evaluate_pit_status(trade_date: str, as_of_date: str | None = None,
                        current_snapshot: bool = False) -> PITStatus:
    """Evaluate PIT status for a given trade_date and data as_of_date.

    Args:
        trade_date: The trading date in YYYY-MM-DD format.
        as_of_date: The date the data became available, or None.
        current_snapshot: Whether this is a current-snapshot-only data point.

    Returns:
        PITStatus enum value.
    """
    if current_snapshot:
        return PITStatus.CURRENT_SNAPSHOT_ONLY
    if as_of_date is None:
        return PITStatus.UNKNOWN_PIT_STATUS
    if as_of_date > trade_date:
        return PITStatus.BLOCKED_FOR_BACKTEST
    return PITStatus.PIT_SAFE
