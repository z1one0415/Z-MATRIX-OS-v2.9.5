"""Event lineage tracing — parent_event_id chain with cycle detection"""
from __future__ import annotations


def build_lineage_record(event: dict) -> dict:
    """Extract lineage metadata from an event."""
    return {
        "event_id": event.get("event_id"),
        "event_type": event.get("event_type"),
        "source_event_id": event.get("source_event_id"),
        "parent_event_id": event.get("parent_event_id"),
        "producer_module": event.get("producer_module"),
        "created_at": event.get("created_at"),
    }


def trace_event_lineage(
    event_id: str,
    events: list[dict],
) -> list[dict]:
    """Trace lineage chain upward via parent_event_id.

    Detects cycles. Stops at missing parent (marks missing_parent=True).
    Returns ordered list of lineage records (first = root).
    """
    event_map = {e.get("event_id", ""): e for e in events}

    chain: list[dict] = []
    visited: set[str] = set()
    current_id: str | None = event_id

    while current_id is not None:
        if current_id in visited:
            chain.append({
                "event_id": current_id,
                "event_type": "CYCLE_DETECTED",
                "missing_parent": False,
            })
            break

        visited.add(current_id)
        current_event = event_map.get(current_id)

        if current_event is None:
            chain.append({
                "event_id": current_id,
                "missing_parent": True,
            })
            break

        chain.append(build_lineage_record(current_event))
        current_id = current_event.get("parent_event_id")

    chain.reverse()
    return chain
