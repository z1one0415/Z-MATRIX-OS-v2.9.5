"""EventStore adapters — build events from existing module outputs

These adapters do NOT append events automatically.
They only package results into EventStore event format.
"""
from __future__ import annotations

from zmatrix.event_store.builders import build_event


def build_paper_ledger_event(paper_entry: dict) -> dict:
    """Build a PaperLedgerEvent from a paper ledger entry.

    Does not append. Does not write Z9. Does not write Hermes memory.
    """
    payload = {
        "ticker": paper_entry.get("ticker", ""),
        "role": paper_entry.get("role", ""),
        "action": paper_entry.get("action", ""),
        "quantity": paper_entry.get("quantity", 0),
        "price": paper_entry.get("price", 0.0),
    }
    return build_event(
        event_type="PaperLedgerEvent",
        producer_module="zmatrix.event_store.adapters.build_paper_ledger_event",
        payload=payload,
    )


def build_outcome_backfill_event(
    outcome: dict,
    parent_event_id: str | None = None,
) -> dict:
    """Build an OutcomeBackfillEvent from an outcome backfill result.

    Does not append. Does not write Z9. Does not write Hermes memory.
    """
    payload = {
        "ticker": outcome.get("ticker", ""),
        "backfill_status": outcome.get("status", ""),
        "prediction_id": outcome.get("prediction_id", ""),
        "result": outcome.get("result", ""),
    }
    return build_event(
        event_type="OutcomeBackfillEvent",
        producer_module="zmatrix.event_store.adapters.build_outcome_backfill_event",
        payload=payload,
        parent_event_id=parent_event_id,
    )


def build_role_classification_event(
    role_result: dict,
    parent_event_id: str | None = None,
) -> dict:
    """Build a RoleClassificationEvent from a stock role classification result.

    Does not append. Does not write Z9. Does not write Hermes memory.
    """
    payload = {
        "ticker": role_result.get("ticker", ""),
        "role": role_result.get("role", ""),
        "b_matrix_score": role_result.get("b_matrix_score"),
        "r_matrix_score": role_result.get("r_matrix_score"),
        "d_matrix_score": role_result.get("d_matrix_score"),
    }
    return build_event(
        event_type="RoleClassificationEvent",
        producer_module="zmatrix.event_store.adapters.build_role_classification_event",
        payload=payload,
        parent_event_id=parent_event_id,
    )
