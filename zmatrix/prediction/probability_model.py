"""Probability model — INV-TG18-01 Sigmoid Shield

CRITICAL: raw_score enters sigmoid FIRST. Coverage/risk/conflict/macro penalties
are applied AFTER in probability space. Never multiply raw_score by coverage before sigmoid.
"""
from __future__ import annotations
import math


def sigmoid(x: float, midpoint: float = 0.0, steepness: float = 0.15) -> float:
    """Standard logistic: 0→0.5, +∞→1.0, -∞→0.0"""
    return 1.0 / (1.0 + math.exp(-(x - midpoint) / steepness))


def fermi_weighted(raw_score: float,
                   coverage_adj: float = 1.0,
                   risk_penalty: float = 0.0,
                   conflict_penalty: float = 0.0,
                   macro_penalty: float = 0.0) -> dict:
    """INV-TG18-01: raw_score→sigmoid, THEN penalties in probability space.

    Args:
        raw_score: aggregated factor score (-20 to +20)
        coverage_adj: 0.0-1.0, evidence coverage multiplier
        risk_penalty: 0.0-1.0, deducted from probability
        conflict_penalty: 0.0-1.0, deducted from probability
        macro_penalty: 0.0-1.0, deducted from probability

    Returns:
        {probability, raw_sigmoid, penalties_applied}
    """
    # Step 1: raw_score → sigmoid (NOT multiplied by coverage)
    raw_sigmoid = sigmoid(raw_score)

    # Step 2: penalties in probability space
    total_penalty = risk_penalty + conflict_penalty + macro_penalty
    total_penalty = min(total_penalty, 0.95)  # never zero out completely

    prob = raw_sigmoid * coverage_adj - total_penalty
    prob = max(0.01, min(0.99, prob))

    return {
        "probability": round(prob, 4),
        "raw_sigmoid": round(raw_sigmoid, 4),
        "penalties": {
            "risk": risk_penalty,
            "conflict": conflict_penalty,
            "macro": macro_penalty,
            "total": total_penalty,
        },
        "coverage_adj": coverage_adj,
    }


def test_sigmoid_shield_extreme():
    """INV-TG18-01 verification: extreme score + heavy penalty must cap ≤0.50"""
    r = fermi_weighted(raw_score=20, coverage_adj=1.0, risk_penalty=0.5, conflict_penalty=0.0, macro_penalty=0.0)
    assert r["probability"] <= 0.50, f"Shield failed: {r['probability']} > 0.50"
    # raw sigmoid at +20 should be near 1.0
    assert r["raw_sigmoid"] > 0.90, f"Unexpected raw_sigmoid: {r['raw_sigmoid']}"


def test_sigmoid_shield_coverage_separate():
    """Coverage adjustment comes AFTER sigmoid, not before"""
    # Correct: sigmoid first, then ×0.3 coverage
    r_correct = fermi_weighted(raw_score=10, coverage_adj=0.3)
    # Wrong would be: sigmoid(10 * 0.3) = sigmoid(3) ≈ 0.88 — much higher
    # Correct yields: sigmoid(10) * 0.3 ≈ 0.76 * 0.3 ≈ 0.23
    assert r_correct["probability"] < 0.40, f"Coverage penalty too weak: {r_correct['probability']}"
