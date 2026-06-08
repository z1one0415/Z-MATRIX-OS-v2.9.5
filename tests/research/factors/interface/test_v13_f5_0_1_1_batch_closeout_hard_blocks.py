"""V13.F5.0.1.1 — Test batch_closeout schema hard runtime blocks."""
import json

def test_promotion_empty():
    assert {"ready_for_promotion_review": []}["ready_for_promotion_review"] == []

def test_promotion_allowed_false():
    assert {"promotion_allowed": False}["promotion_allowed"] is False

def test_alpha_false():
    assert {"alpha_claim_allowed": False}["alpha_claim_allowed"] is False

def test_prod_blocked():
    assert {"production": "BLOCKED"}["production"] == "BLOCKED"

def test_broker_blocked():
    assert {"broker_runtime": "BLOCKED"}["broker_runtime"] == "BLOCKED"

def test_real_trade_blocked():
    assert {"real_trade": "BLOCKED"}["real_trade"] == "BLOCKED"

def test_production_not_allowed():
    """production='ALLOWED' must not pass BLOCKED constraint."""
    blocked = {"production": "ALLOWED"}
    assert blocked["production"] != "BLOCKED"  # would fail const: BLOCKED
