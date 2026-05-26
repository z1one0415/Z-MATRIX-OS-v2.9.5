"""EventStore → Hermes Preview Bridge — build MemoryCandidate from outcome events"""
from __future__ import annotations

from zmatrix.hermes_kernel.schemas import HERMES_KERNEL_SAFETY
from zmatrix.hermes_kernel.memory_candidate import build_memory_candidate_preview


def build_memory_candidate_from_outcome_event(
    outcome_event: dict,
    related_events: list[dict] | None = None,
) -> dict:
    """Build a MemoryCandidate preview from an OutcomeBackfillEvent.

    Logic:
    - If actual_return_t20 is negative or max_drawdown_t20 is high → generate candidate
    - Losses/drawdowns MAY generate candidates but MUST NOT generate Approved Heuristics
    - If insufficient data → risk_of_overfitting = HIGH
    """
    payload = outcome_event.get("payload", {})
    ticker = payload.get("ticker", "unknown")
    ret_t20 = payload.get("actual_return_t20")
    dd_t20 = payload.get("max_drawdown_t20")

    # Determine severity and risk
    has_loss = ret_t20 is not None and ret_t20 < 0
    has_drawdown = dd_t20 is not None and dd_t20 > 5.0
    has_insufficient_data = ret_t20 is None and dd_t20 is None

    if has_insufficient_data:
        confidence = "LOW"
        risk_of_overfitting = "HIGH"
        title = f"insufficient outcome data: {ticker}"
        proposed_rule = f"collect more outcome data for {ticker} before generating heuristic"
    elif has_loss and has_drawdown:
        confidence = "MEDIUM"
        risk_of_overfitting = "MEDIUM"
        title = f"loss with drawdown: {ticker} (ret={ret_t20}, dd={dd_t20})"
        proposed_rule = f"review entry conditions for {ticker} when max_drawdown > {dd_t20}"
    elif has_loss:
        confidence = "LOW"
        risk_of_overfitting = "HIGH"
        title = f"return loss: {ticker} (ret={ret_t20})"
        proposed_rule = f"monitor {ticker} for recovery or exit"
    else:
        confidence = "LOW"
        risk_of_overfitting = "LOW"
        title = f"outcome neutral: {ticker}"
        proposed_rule = f"continue observing {ticker}"

    evidence_summary = f"outcome_id={outcome_event.get('event_id','')}"
    if related_events:
        evidence_summary += f", {len(related_events)} related events"

    preview = build_memory_candidate_preview(
        source_event_id=outcome_event.get("event_id", ""),
        candidate_type="outcome_derived",
        title=title,
        proposed_rule=proposed_rule,
        evidence_summary=evidence_summary,
        confidence=confidence,
        risk_of_overfitting=risk_of_overfitting,
    )

    return preview
