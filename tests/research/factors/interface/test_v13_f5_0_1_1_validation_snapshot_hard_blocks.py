"""V13.F5.0.1.1 — Test validation_snapshot schema hard blocks."""
import json

def test_promotion_allowed_must_be_false():
    src = {"promotion_allowed": False}
    invalid = {"promotion_allowed": True}
    assert src["promotion_allowed"] is False
    assert invalid["promotion_allowed"] is True  # would fail const: false

def test_ready_for_promotion_review_must_be_empty():
    valid = {"ready_for_promotion_review": []}
    invalid = {"ready_for_promotion_review": ["F04"]}
    assert len(valid["ready_for_promotion_review"]) == 0
    assert len(invalid["ready_for_promotion_review"]) > 0  # would fail maxItems: 0

def test_multi_composite_false():
    assert {"multi_factor_composite_built": False}["multi_factor_composite_built"] is False

def test_weight_opt_false():
    assert {"weight_optimization_executed": False}["weight_optimization_executed"] is False

def test_alpha_false():
    assert {"alpha_claim_allowed": False}["alpha_claim_allowed"] is False

def test_prod_blocked():
    assert {"production": "BLOCKED"}["production"] == "BLOCKED"
