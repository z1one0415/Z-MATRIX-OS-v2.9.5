"""R06_REFLEXIVITY_NARRATIVE — Narrative vs fundamental feedback loops

Methodology:
    Inspired by Soros' theory of reflexivity. Detects divergence between
    narrative strength and fundamental trends. When narrative runs ahead
    of fundamentals (or vice versa), a feedback loop may form — and the
    wider the divergence, the higher the risk.

Scoring:
    aligned (no divergence)          → 80
    mild divergence                  → 50
    strong divergence               → 20
"""
from __future__ import annotations
from zmatrix.research_council.reviewers import ReviewerOutput

REVIEWER_CONFIG = {
    "reviewer_id": "R06_REFLEXIVITY_NARRATIVE",
    "methodology": "Narrative vs fundamental feedback loops",
    "required_evidence": ["source", "narrative_strength", "fundamental_trend", "sentiment_divergence"],
}

def review(facts: dict | None = None) -> ReviewerOutput:
    """Deterministic reflexivity/narrative review."""
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
    divergence = str(facts.get("sentiment_divergence", "")).lower()
    if divergence in ("aligned", "none", "low"):
        score = 80
    elif divergence in ("mild", "moderate", "mild_divergence"):
        score = 50
    elif divergence in ("strong", "high", "strong_divergence"):
        score = 20
    else:
        score = 50  # default: unknown = mild
    trace = {
        "reviewer": REVIEWER_CONFIG["reviewer_id"],
        "method": REVIEWER_CONFIG["methodology"],
        "input_facts": dict(facts),
        "calculation": f"divergence={divergence} → score={score}",
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
