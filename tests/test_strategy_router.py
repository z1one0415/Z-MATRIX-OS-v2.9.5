"""Tests for Strategy Router."""
from zmatrix.strategy.strategy_router import route_strategy
def test_mainboard_reversal():
    r = route_strategy("MAINBOARD","REVERSAL")
    assert r["strategy_family"] == "REVERSAL_REPAIR"
    assert r["not_trade_signal"] is True
def test_star_momentum():
    r = route_strategy("STAR","MOMENTUM")
    assert r["strategy_family"] == "B_MATRIX_MOMENTUM"
def test_chinext_transition():
    r = route_strategy("CHINEXT","TRANSITION")
    assert r["strategy_family"] == "CONFIRMED_MOMENTUM_OR_WAIT"
