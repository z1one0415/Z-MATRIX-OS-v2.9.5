"""Outcome Event Adapter — build OutcomeBackfillEvent, no append"""
from __future__ import annotations
from zmatrix.event_store.builders import build_event

def build_outcome_event(outcome_record: dict) -> dict:
    """Build OutcomeBackfillEvent from outcome record. No append."""
    return build_event(
        event_type="OutcomeBackfillEvent",
        producer_module="zmatrix.paper_outcome.event_adapter",
        payload={
            "outcome_id": outcome_record.get("outcome_id", ""),
            "paper_id": outcome_record.get("paper_id", ""),
            "ticker": outcome_record.get("ticker", ""),
            "actual_return_t5": outcome_record.get("actual_return_t5"),
            "actual_return_t20": outcome_record.get("actual_return_t20"),
            "actual_return_t60": outcome_record.get("actual_return_t60"),
            "max_drawdown_t20": outcome_record.get("max_drawdown_t20"),
            "outcome_status": outcome_record.get("outcome_status", ""),
            "invalidation_triggered": outcome_record.get("invalidation_triggered", False),
        },
    )
