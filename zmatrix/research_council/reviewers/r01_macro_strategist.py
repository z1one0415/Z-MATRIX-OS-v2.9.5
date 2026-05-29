"""R01_MACRO_STRATEGIST — Inversion: what macro consensus is wrong?

Methodology:
    Instead of following macro consensus, this reviewer actively questions
    prevailing narratives. It asks: what if the consensus is wrong, and in
    which direction? Scoring increases with evidence depth — each additional
    fact beyond required evidence adds confidence.

Scoring:
    Linear accumulation: +10 per fact present, max 100.
"""
from __future__ import annotations
from zmatrix.research_council.reviewers import ReviewerOutput

REVIEWER_CONFIG = {
    "reviewer_id": "R01_MACRO_STRATEGIST",
    "methodology": "Inversion: what macro consensus is wrong?",
    "required_evidence": ["source", "macro_cycle_phase", "consensus_view"],
}

def review(facts: dict | None = None) -> ReviewerOutput:
    """Deterministic macro consensus inversion review."""
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
    score = min(100, len(facts) * 10)
    trace = {
        "reviewer": REVIEWER_CONFIG["reviewer_id"],
        "method": REVIEWER_CONFIG["methodology"],
        "input_facts": dict(facts),
        "calculation": f"len(facts)={len(facts)} * 10 = {score} (capped 100)",
    }
    return ReviewerOutput(
        reviewer_id=REVIEWER_CONFIG["reviewer_id"],
        facts=facts,
        deterministic_score=score,
        score_trace=trace,
        review_status="RESEARCH_SUPPORT",
        real_trade_allowed=False,
        broker_order_allowed=False,
    )
