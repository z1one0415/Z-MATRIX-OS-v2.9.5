# allowlist: forbidden-token-definition
"""R12_ACCOUNT_SURVIVAL — Risk budget + drawdown + survival probability

Methodology:
    The ultimate risk manager. Evaluates whether the strategy can survive
    adverse conditions by checking risk budget remaining, max drawdown, and
    statistical survival probability. No alpha matters if the account dies.

Scoring:
    survival_probability >= 0.95 → +60, >= 0.85 → +40
    max_drawdown_pct <= 10      → +30
    risk_budget_remaining >= 50% → +10
    Max 100.
"""
from __future__ import annotations
from zmatrix.research_council.reviewers import ReviewerOutput

REVIEWER_CONFIG = {
    "reviewer_id": "R12_ACCOUNT_SURVIVAL",
    "methodology": "Risk budget + drawdown + survival probability",
    "required_evidence": ["source", "risk_budget_remaining_pct", "max_drawdown_pct", "survival_probability"],
}

SCORING_CONFIG = {
    "score_min": 0,
    "score_max": 100,
    "weights": {
        "drawdown_risk": 0.35,
        "risk_budget": 0.35,
        "position_concentration": 0.3
    },
    "thresholds": {
        "safe": 80,
        "caution": 45,
        "danger": 15
    }
}

def review(facts: dict | None = None) -> ReviewerOutput:
    """Deterministic account survival review."""
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
    survival = facts.get("survival_probability", 0)
    drawdown = facts.get("max_drawdown_pct", 100)
    budget = facts.get("risk_budget_remaining_pct", 0)
    survival_score = 60 if survival >= 0.95 else (40 if survival >= 0.85 else 0)
    drawdown_score = 30 if drawdown <= 10 else 0
    budget_score = 10 if budget >= 50 else 0
    score = min(100, survival_score + drawdown_score + budget_score)
    trace = {
        "reviewer": REVIEWER_CONFIG["reviewer_id"],
        "method": REVIEWER_CONFIG["methodology"],
        "input_facts": dict(facts),
        "calculation": f"survival={survival} → {survival_score}; "
                       f"drawdown={drawdown}% → {drawdown_score}; "
                       f"budget={budget}% → {budget_score}; sum={score} (capped 100)",
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
