"""R04_QUALITY_GROWTH — Quality compounder lifecycle stage

Methodology:
    Assesses a company's position in the quality compounder lifecycle.
    Combines lifecycle stage with ROE (5yr average) and reinvestment rate
    to determine the quality-growth compounder score.

Scoring:
    lifecycle="early"  → 40, "growth" → 60, "mature" → 30, "decline" → 10
    roe_5yr_avg >= 20 → +40, >= 15 → +25
    Max 100.
"""
from __future__ import annotations
from zmatrix.research_council.reviewers import ReviewerOutput

REVIEWER_CONFIG = {
    "reviewer_id": "R04_QUALITY_GROWTH",
    "methodology": "Quality compounder lifecycle stage",
    "required_evidence": ["source", "lifecycle_stage", "roe_5yr_avg", "reinvestment_rate"],
}

LIFECYCLE_SCORES = {"early": 40, "growth": 60, "mature": 30, "decline": 10}

def review(facts: dict | None = None) -> ReviewerOutput:
    """Deterministic quality growth lifecycle review."""
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
    stage = facts.get("lifecycle_stage", "mature")
    life_score = LIFECYCLE_SCORES.get(stage, 30)
    roe = facts.get("roe_5yr_avg", 0)
    roe_score = 40 if roe >= 20 else (25 if roe >= 15 else 0)
    score = min(100, life_score + roe_score)
    trace = {
        "reviewer": REVIEWER_CONFIG["reviewer_id"],
        "method": REVIEWER_CONFIG["methodology"],
        "input_facts": dict(facts),
        "calculation": f"lifecycle={stage} → life_score={life_score}; "
                       f"roe={roe}% → roe_score={roe_score}; sum={score} (capped 100)",
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
