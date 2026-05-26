"""Working Context Preview — build working context from EventStore events (read-only)"""
from __future__ import annotations
from datetime import datetime, timezone

from zmatrix.hermes_kernel.schemas import HERMES_KERNEL_SAFETY

_WORKING_CONTEXT_TYPES = {"stock_review", "paper_decision", "outcome_review", "risk_review", "unknown"}


def build_working_context_from_events(
    *,
    events: list[dict],
    ticker: str | None = None,
    role: str | None = None,
    chain: str | None = None,
) -> dict:
    """Build working context preview from EventStore events.

    Extracts event_ids, ticker, role, recent outcomes, recent paper decisions,
    and recent risk events from the provided events list.

    Read-only: does not write EventStore, Hermes memory, or Z9.
    """
    if ticker and role:
        context_type = "paper_decision"
    elif ticker:
        context_type = "stock_review"
    elif chain:
        context_type = "risk_review"
    else:
        context_type = "unknown"

    event_ids = [e.get("event_id", "") for e in events if e.get("event_id")]
    context_id = hashlib.sha256(
        f"{ticker or ''}{role or ''}{chain or ''}{len(events)}".encode()
    ).hexdigest()[:16]

    outcomes = [e for e in events if e.get("event_type") == "OutcomeBackfillEvent"]
    papers = [e for e in events if e.get("event_type") == "PaperLedgerEvent"]
    risks = [e for e in events if e.get("event_type") == "RiskEvent"]

    summary_parts = []
    if outcomes:
        summary_parts.append(f"{len(outcomes)} outcome(s)")
    if papers:
        summary_parts.append(f"{len(papers)} paper decision(s)")
    if risks:
        summary_parts.append(f"{len(risks)} risk event(s)")
    summary = ", ".join(summary_parts) if summary_parts else "No related events"

    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    return {
        "context": {
            "context_id": context_id,
            "context_type": context_type,
            "ticker": ticker or "",
            "chain": chain or "",
            "sector": "",
            "role": role or "",
            "event_ids": event_ids,
            "summary": summary,
            "created_at": now,
        },
        "extracted_outcomes": outcomes,
        "extracted_papers": papers,
        "extracted_risks": risks,
        "safety": dict(HERMES_KERNEL_SAFETY),
        "preview_only": True,
        "write_allowed": False,
        "hermes_memory_write_allowed": False,
    }


import hashlib
