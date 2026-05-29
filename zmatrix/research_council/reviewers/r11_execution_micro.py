"""R11_EXECUTION_MICRO — Microstructure + fillability + route analysis

Methodology:
    Assesses execution feasibility. Combines average daily volume, bid-ask
    spread, and fill probability to determine whether a position can be
    entered/exited without excessive market impact.

Scoring:
    fill_probability >= 0.95 → +60, >= 0.80 → +40
    bid_ask_spread_bps <= 5  → +30, <= 20    → +15
    Max 100.
"""
from __future__ import annotations
from zmatrix.research_council.reviewers import ReviewerOutput

REVIEWER_CONFIG = {
    "reviewer_id": "R11_EXECUTION_MICRO",
    "methodology": "Microstructure + fillability + route analysis",
    "required_evidence": ["source", "avg_daily_volume", "bid_ask_spread_bps", "fill_probability"],
}

def review(facts: dict | None = None) -> ReviewerOutput:
    """Deterministic execution microstructure review."""
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
    fill_prob = facts.get("fill_probability", 0)
    spread = facts.get("bid_ask_spread_bps", 100)
    fill_score = 60 if fill_prob >= 0.95 else (40 if fill_prob >= 0.80 else 0)
    spread_score = 30 if spread <= 5 else (15 if spread <= 20 else 0)
    score = min(100, fill_score + spread_score)
    trace = {
        "reviewer": REVIEWER_CONFIG["reviewer_id"],
        "method": REVIEWER_CONFIG["methodology"],
        "input_facts": dict(facts),
        "calculation": f"fill_prob={fill_prob} → fill_score={fill_score}; "
                       f"spread={spread}bps → spread_score={spread_score}; sum={score} (capped 100)",
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
