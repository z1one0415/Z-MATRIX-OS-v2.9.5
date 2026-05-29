"""R02_MARGIN_OF_SAFETY — Moslow framework: intrinsic value gap

Methodology:
    Applies the Moslow margin-of-safety framework. The core question: how
    large is the gap between estimated intrinsic value and current market
    price? A larger margin of safety (mos_pct) means greater downside
    protection.

Scoring:
    mos_pct >= 30  → 80
    mos_pct >= 20  → 60
    mos_pct >= 10  → 40
    else           → 20
"""
from __future__ import annotations
from zmatrix.research_council.reviewers import ReviewerOutput

REVIEWER_CONFIG = {
    "reviewer_id": "R02_MARGIN_OF_SAFETY",
    "methodology": "Moslow framework: intrinsic value gap",
    "required_evidence": ["source", "intrinsic_value_est", "market_price", "mos_pct"],
}

SCORING_CONFIG = {
    "score_min": 0,
    "score_max": 100,
    "weights": {
        "valuation_gap": 0.5,
        "downside_buffer": 0.3,
        "balance_sheet": 0.2
    },
    "thresholds": {
        "deep_value": 80,
        "fair_value": 50,
        "overvalued": 20
    }
}

def review(facts: dict | None = None) -> ReviewerOutput:
    """Deterministic margin of safety review."""
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
    mos = facts.get("mos_pct", 0)
    if mos >= 30:
        score = 80
    elif mos >= 20:
        score = 60
    elif mos >= 10:
        score = 40
    else:
        score = 20
    trace = {
        "reviewer": REVIEWER_CONFIG["reviewer_id"],
        "method": REVIEWER_CONFIG["methodology"],
        "input_facts": dict(facts),
        "calculation": f"mos_pct={mos} → score={score}",
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
