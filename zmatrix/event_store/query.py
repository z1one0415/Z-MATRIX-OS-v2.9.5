"""EventStore query helpers — filter by type, ticker, producer"""
from __future__ import annotations


def filter_events_by_type(events: list[dict], event_type: str) -> list[dict]:
    """Filter events by exact event_type match."""
    return [e for e in events if e.get("event_type") == event_type]


def filter_events_by_ticker(events: list[dict], ticker: str) -> list[dict]:
    """Filter events by ticker in payload.

    Not all events have a ticker — skip those without.
    """
    results = []
    for e in events:
        payload = e.get("payload", {})
        if isinstance(payload, dict) and payload.get("ticker") == ticker:
            results.append(e)
    return results


def filter_events_by_producer(
    events: list[dict], producer_module: str
) -> list[dict]:
    """Filter events by producer_module."""
    return [e for e in events if e.get("producer_module") == producer_module]
