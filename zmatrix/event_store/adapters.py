"""EventStore adapters — build events from existing module outputs

These adapters do NOT append events automatically.
They only package results into EventStore event format.
"""
from __future__ import annotations

from zmatrix.event_store.builders import build_event


def build_paper_ledger_event(paper_entry: dict) -> dict:
    """Build a PaperLedgerEvent from a paper ledger entry.

    Compatible with v2.9.9 paper ledger schema.
    Does not append. Does not write Z9. Does not write Hermes memory.
    """
    payload = {
        "paper_id": paper_entry.get("paper_id", ""),
        "ticker": paper_entry.get("ticker", ""),
        "role": paper_entry.get("role", ""),
        "entry_date": paper_entry.get("entry_date", ""),
        "entry_price": paper_entry.get("entry_price"),
        "paper_action": paper_entry.get("paper_action", paper_entry.get("action", "")),
        "target_horizon": paper_entry.get("target_horizon", ""),
        "max_loss_plan": paper_entry.get("max_loss_plan"),
        "invalidation_condition": paper_entry.get("invalidation_condition", ""),
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

    Compatible with v2.9.9 outcome fields.
    Does not append. Does not write Z9. Does not write Hermes memory.
    """
    payload = {
        "paper_id": outcome.get("paper_id", ""),
        "ticker": outcome.get("ticker", ""),
        "entry_date": outcome.get("entry_date", ""),
        "actual_return_t5": outcome.get("actual_return_t5"),
        "actual_return_t20": outcome.get("actual_return_t20"),
        "actual_return_t60": outcome.get("actual_return_t60"),
        "max_drawdown_t20": outcome.get("max_drawdown_t20"),
        "max_drawdown_t60": outcome.get("max_drawdown_t60"),
        "outcome_status": outcome.get("outcome_status", outcome.get("status", "")),
        "error_type": outcome.get("error_type", ""),
        "review_note": outcome.get("review_note", ""),
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
