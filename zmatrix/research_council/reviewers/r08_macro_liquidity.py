"""R08_MACRO_LIQUIDITY — Macro liquidity cycle alignment

Methodology:
    Evaluates whether current macro liquidity conditions are favorable.
    Tracks credit spreads, capital flow direction, and the liquidity cycle
    phase to determine the environment's support for risk assets.

Scoring:
    liquidity_cycle_phase:
        "expansion"  → 70
        "neutral"    → 50
        "contraction"→ 20
"""
from __future__ import annotations
from zmatrix.research_council.reviewers import ReviewerOutput

REVIEWER_CONFIG = {
    "reviewer_id": "R08_MACRO_LIQUIDITY",
    "methodology": "Macro liquidity cycle alignment",
    "required_evidence": ["source", "liquidity_cycle_phase", "credit_spread", "capital_flow_direction"],
}

PHASE_SCORES = {"expansion": 70, "neutral": 50, "contraction": 20}

SCORING_CONFIG = {
    "score_min": 0,
    "score_max": 100,
    "weights": {
        "credit_cycle": 0.35,
        "market_liquidity": 0.35,
        "risk_appetite": 0.3
    },
    "thresholds": {
        "expansion": 80,
        "neutral": 50,
        "contraction": 20
    }
}

def review(facts: dict | None = None) -> ReviewerOutput:
    """Deterministic macro liquidity review."""
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
    phase = facts.get("liquidity_cycle_phase", "neutral")
    score = PHASE_SCORES.get(phase, 50)
    trace = {
        "reviewer": REVIEWER_CONFIG["reviewer_id"],
        "method": REVIEWER_CONFIG["methodology"],
        "input_facts": dict(facts),
        "calculation": f"liquidity_cycle_phase={phase} → score={score}",
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
