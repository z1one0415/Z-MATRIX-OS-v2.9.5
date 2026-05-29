# allowlist: forbidden-token-definition
"""R09_FACTOR_VALIDITY — Factor IC decay + regime dependency

Methodology:
    Tests whether a factor signal remains valid in the current regime.
    Tracks recent information coefficient (IC), IC decay rate, and regime
    alignment. Decaying IC in a misaligned regime is a red flag.

Scoring:
    factor_ic_recent >= 0.05 → +60, >= 0.03 → +40
    factor_ic_decay_rate = "low" → +30, "moderate" → +15
    regime_alignment = True → +10
    Max 100.
"""
from __future__ import annotations
from zmatrix.research_council.reviewers import ReviewerOutput

REVIEWER_CONFIG = {
    "reviewer_id": "R09_FACTOR_VALIDITY",
    "methodology": "Factor IC decay + regime dependency",
    "required_evidence": ["source", "factor_ic_recent", "factor_ic_decay_rate", "regime_alignment"],
}

SCORING_CONFIG = {
    "score_min": 0,
    "score_max": 100,
    "weights": {
        "ic": 0.35,
        "rankic": 0.25,
        "decile_spread": 0.2,
        "sample_size": 0.2
    },
    "thresholds": {
        "robust": 75,
        "decaying": 45,
        "broken": 15
    }
}

def review(facts: dict | None = None) -> ReviewerOutput:
    """Deterministic factor validity review."""
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
    ic = facts.get("factor_ic_recent", 0)
    decay = str(facts.get("factor_ic_decay_rate", "")).lower()
    aligned = facts.get("regime_alignment", False)
    ic_score = 60 if ic >= 0.05 else (40 if ic >= 0.03 else 0)
    decay_score = 30 if decay == "low" else (15 if decay == "moderate" else 0)
    regime_score = 10 if aligned else 0
    score = min(100, ic_score + decay_score + regime_score)
    trace = {
        "reviewer": REVIEWER_CONFIG["reviewer_id"],
        "method": REVIEWER_CONFIG["methodology"],
        "input_facts": dict(facts),
        "calculation": f"ic={ic} → ic_score={ic_score}; "
                       f"decay={decay} → decay_score={decay_score}; "
                       f"aligned={aligned} → regime_score={regime_score}; sum={score} (capped 100)",
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
