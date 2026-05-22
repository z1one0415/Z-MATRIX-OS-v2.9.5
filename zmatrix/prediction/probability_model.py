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
                   risk_penalty: float = 1.0,
                   conflict_penalty: float = 1.0,
                   macro_probability_gate: float = 1.0) -> dict:
    """INV-TG18-01: raw_score→sigmoid, THEN multiplicative penalties in probability space.

    risk_penalty=0.5 means "keep 50% of probability after risk discount".
    All penalties are multiplicative (not additive subtraction).
    """
    # Step 1: raw_score → sigmoid (NOT multiplied by coverage)
    raw_sigmoid = sigmoid(raw_score)

    # Step 2: multiplicative penalties in probability space
    prob = raw_sigmoid * coverage_adj * risk_penalty * conflict_penalty * macro_probability_gate
    prob = max(0.01, min(0.99, prob))

    return {
        "probability": round(prob, 4),
        "raw_sigmoid": round(raw_sigmoid, 4),
        "penalties": {
            "risk_retention": risk_penalty,
            "conflict_retention": conflict_penalty,
            "macro_gate": macro_probability_gate,
        },
        "coverage_adj": coverage_adj,
    }


def test_sigmoid_shield_extreme():
    """INV-TG18-01: extreme + heavy penalty must cap ≤0.50"""
    r = fermi_weighted(raw_score=20, coverage_adj=1.0, risk_penalty=0.5)
    assert r["probability"] <= 0.50, f"Shield failed: {r['probability']} > 0.50"
    assert r["raw_sigmoid"] > 0.90


def test_sigmoid_shield_coverage_separate():
    """Coverage comes AFTER sigmoid, not before"""
    r = fermi_weighted(raw_score=10, coverage_adj=0.3)
    assert r["probability"] < 0.40, f"Coverage penalty too weak: {r['probability']}"
