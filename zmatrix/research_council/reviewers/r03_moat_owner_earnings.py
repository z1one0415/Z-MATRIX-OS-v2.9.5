# allowlist: forbidden-token-definition
"""R03_MOAT_OWNER_EARNINGS — Moat durability + owner earnings yield

Methodology:
    Evaluates the durability of a company's competitive moat combined with
    its owner earnings yield. A wide, long-lasting moat paired with high
    owner earnings yield indicates strong structural advantage.

Scoring:
    moat_durability >= 10 years → +50, >= 5 years → +30
    owner_earnings_yield >= 8%     → +50, >= 5%     → +30
    Sum capped at 100.
"""
from __future__ import annotations
from zmatrix.research_council.reviewers import ReviewerOutput

REVIEWER_CONFIG = {
    "reviewer_id": "R03_MOAT_OWNER_EARNINGS",
    "methodology": "Moat durability + owner earnings yield",
    "required_evidence": ["source", "moat_type", "moat_durability_years", "owner_earnings_yield"],
}

SCORING_CONFIG = {
    "score_min": 0,
    "score_max": 100,
    "weights": {
        "moat_durability": 0.45,
        "owner_earnings": 0.35,
        "pricing_power": 0.2
    },
    "thresholds": {
        "wide_moat": 80,
        "narrow_moat": 50,
        "no_moat": 20
    }
}

def review(facts: dict | None = None) -> ReviewerOutput:
    """Deterministic moat + owner earnings review."""
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
    durability = facts.get("moat_durability_years", 0)
    earnings_yield = facts.get("owner_earnings_yield", 0)
    moat_score = 50 if durability >= 10 else (30 if durability >= 5 else 0)
    yield_score = 50 if earnings_yield >= 8 else (30 if earnings_yield >= 5 else 0)
    score = min(100, moat_score + yield_score)
    trace = {
        "reviewer": REVIEWER_CONFIG["reviewer_id"],
        "method": REVIEWER_CONFIG["methodology"],
        "input_facts": dict(facts),
        "calculation": f"moat_durability={durability}y → moat_score={moat_score}; "
                       f"owner_earnings_yield={earnings_yield}% → yield_score={yield_score}; "
                       f"sum={score} (capped 100)",
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
