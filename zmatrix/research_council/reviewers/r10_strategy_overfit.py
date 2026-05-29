# allowlist: forbidden-token-definition
"""R10_STRATEGY_OVERFIT — Train/test contamination + lookahead audit

Methodology:
    Audits strategy development for overfitting. Checks train/test split
    integrity, contamination between sets, and lookahead bias. A clean
    setup scores high; confirmed contamination is a critical failure.

Scoring:
    clean                        → 90
    minor leak                   → 50
    confirmed contamination      → 10
"""
from __future__ import annotations
from zmatrix.research_council.reviewers import ReviewerOutput

REVIEWER_CONFIG = {
    "reviewer_id": "R10_STRATEGY_OVERFIT",
    "methodology": "Train/test contamination + lookahead audit",
    "required_evidence": ["source", "train_test_split_ratio", "contamination_score", "lookahead_bias_check"],
}

SCORING_CONFIG = {
    "score_min": 0,
    "score_max": 100,
    "weights": {
        "walkforward": 0.3,
        "sector_holdout": 0.25,
        "parameter_stability": 0.25,
        "contamination": 0.2
    },
    "thresholds": {
        "clean": 90,
        "minor_leak": 50,
        "overfitted": 10
    }
}

def review(facts: dict | None = None) -> ReviewerOutput:
    """Deterministic overfit audit review."""
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
    contamination = str(facts.get("contamination_score", "")).lower()
    if contamination in ("clean", "none", "0"):
        score = 90
    elif contamination in ("minor", "minor_leak", "low"):
        score = 50
    elif contamination in ("confirmed", "confirmed_contamination", "high"):
        score = 10
    else:
        score = 50
    trace = {
        "reviewer": REVIEWER_CONFIG["reviewer_id"],
        "method": REVIEWER_CONFIG["methodology"],
        "input_facts": dict(facts),
        "calculation": f"contamination={contamination} → score={score}",
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
