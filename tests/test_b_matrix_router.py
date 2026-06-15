"""Tests for B-MATRIX Router."""
from zmatrix.strategy.b_matrix_router import is_b_matrix_search_allowed
def test_star_momentum_allowed():
    r = is_b_matrix_search_allowed("STAR","MOMENTUM")
    assert r["b_matrix_search_status"] == "ALLOWED"
    assert r["search_priority"] == "HIGH"
def test_mainboard_reversal_blocked():
    r = is_b_matrix_search_allowed("MAINBOARD","REVERSAL")
    assert r["b_matrix_search_status"] == "BLOCKED"
def test_chinext_momentum_allowed():
    r = is_b_matrix_search_allowed("CHINEXT","MOMENTUM")
    assert r["b_matrix_search_status"] == "ALLOWED"
