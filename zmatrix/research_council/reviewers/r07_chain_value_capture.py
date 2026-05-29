# allowlist: forbidden-token-definition
"""R07_CHAIN_VALUE_CAPTURE — Industry chain value capture positioning

Methodology:
    Analyzes a company's position within its industry value chain and its
    ability to capture value. Core technology providers with pricing power
    capture the most value; commodity players the least. Pricing power
    provides a bonus modifier.

Scoring:
    chain_position:
        "core_tech"   → 60
        "key_supplier"→ 45
        "integrator"  → 30
        "commodity"   → 15
    pricing_power bonus:
        "high"        → +20
        "medium"      → +10
        "low"         → +0
    Max 100.
"""
from __future__ import annotations
from zmatrix.research_council.reviewers import ReviewerOutput

REVIEWER_CONFIG = {
    "reviewer_id": "R07_CHAIN_VALUE_CAPTURE",
    "methodology": "Industry chain value capture positioning",
    "required_evidence": ["source", "chain_position", "value_add_pct", "pricing_power"],
}

POSITION_SCORES = {"core_tech": 60, "key_supplier": 45, "integrator": 30, "commodity": 15}
PRICING_BONUS = {"high": 20, "medium": 10, "low": 0}

SCORING_CONFIG = {
    "score_min": 0,
    "score_max": 100,
    "weights": {
        "chain_position": 0.4,
        "value_capture": 0.35,
        "bargaining_power": 0.25
    },
    "thresholds": {
        "core_tech": 85,
        "key_supplier": 55,
        "commodity": 25
    }
}

def review(facts: dict | None = None) -> ReviewerOutput:
    """Deterministic chain value capture review."""
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
    position = facts.get("chain_position", "commodity")
    base = POSITION_SCORES.get(position, 15)
    pricing = facts.get("pricing_power", "low")
    bonus = PRICING_BONUS.get(pricing, 0)
    score = min(100, base + bonus)
    trace = {
        "reviewer": REVIEWER_CONFIG["reviewer_id"],
        "method": REVIEWER_CONFIG["methodology"],
        "input_facts": dict(facts),
        "calculation": f"chain_position={position} → base={base}; "
                       f"pricing_power={pricing} → bonus={bonus}; sum={score} (capped 100)",
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
