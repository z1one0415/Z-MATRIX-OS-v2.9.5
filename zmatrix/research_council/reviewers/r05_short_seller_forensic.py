"""R05_SHORT_SELLER_FORENSIC — Forensic accounting attack vectors

Methodology:
    Applies short-seller forensic accounting checks. Examines receivables
    quality, cash flow matching, and related-party transactions for signs
    of earnings manipulation or accounting irregularities.

Scoring:
    all_clean     → 90
    1 flag        → 50
    2+ flags      → 20
"""
from __future__ import annotations
from zmatrix.research_council.reviewers import ReviewerOutput

REVIEWER_CONFIG = {
    "reviewer_id": "R05_SHORT_SELLER_FORENSIC",
    "methodology": "Forensic accounting attack vectors",
    "required_evidence": ["source", "receivables_quality", "cashflow_match", "related_party_check"],
}

def review(facts: dict | None = None) -> ReviewerOutput:
    """Deterministic forensic accounting review."""
    facts = facts or {}
    required = REVIEWER_CONFIG["required_evidence"]
    missing = [f for f in required if f not in facts]
    if missing:
        return ReviewerOutput(
            reviewer_id=REVIEWER_CONFIG["reviewer_id"],
            facts=facts,
            missing_evidence=missing,
            review_status="DATA_INSUFFICIENT",
            real_trade_allowed=False,
            broker_order_allowed=False,
        )
    checks = [
        facts.get("receivables_quality", ""),
        facts.get("cashflow_match", ""),
        facts.get("related_party_check", ""),
    ]
    flags = sum(1 for c in checks if c == "flag" or "flag" in str(c).lower())
    if flags == 0:
        score = 90
    elif flags == 1:
        score = 50
    else:
        score = 20
    trace = {
        "reviewer": REVIEWER_CONFIG["reviewer_id"],
        "method": REVIEWER_CONFIG["methodology"],
        "input_facts": dict(facts),
        "calculation": f"checks={checks}, flags={flags} → score={score}",
    }
    return ReviewerOutput(
        reviewer_id=REVIEWER_CONFIG["reviewer_id"],
        facts=facts,
        deterministic_score=float(score),
        score_trace=trace,
        review_status="RESEARCH_SUPPORT",
        real_trade_allowed=False,
        broker_order_allowed=False,
    )
