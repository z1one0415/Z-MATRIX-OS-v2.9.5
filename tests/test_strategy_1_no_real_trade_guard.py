"""Strategy.1: no real trade guard regression — scans for forbidden actions."""
import re
FORBIDDEN = ["BUY", "SELL", "ADD", "AUTO_TRADE", "MARKET_ORDER"]

def test_no_forbidden_in_board_classifier():
    src = open("zmatrix/strategy/board_classifier.py").read()
    for w in FORBIDDEN:
        assert w not in src, f"{w} found in board_classifier.py"

def test_no_forbidden_in_regime_detector():
    src = open("zmatrix/strategy/regime_detector.py").read()
    for w in FORBIDDEN:
        assert w not in src, f"{w} found in regime_detector.py"

def test_no_forbidden_in_strategy_router():
    src = open("zmatrix/strategy/strategy_router.py").read()
    for w in FORBIDDEN:
        assert w not in src, f"{w} found in strategy_router.py"

def test_no_forbidden_in_b_matrix_router():
    src = open("zmatrix/strategy/b_matrix_router.py").read()
    for w in FORBIDDEN:
        assert w not in src, f"{w} found in b_matrix_router.py"

def test_no_forbidden_in_interpretation():
    src = open("zmatrix/prediction/board_regime_interpretation.py").read()
    for w in FORBIDDEN:
        assert w not in src, f"{w} found in board_regime_interpretation.py"

def test_no_forbidden_in_context():
    src = open("zmatrix/strategy/board_regime_context.py").read()
    for w in FORBIDDEN:
        assert w not in src, f"{w} found in board_regime_context.py"

def test_safety_contract_asserts():
    from zmatrix.strategy.strategy_contracts import assert_strategy_safety
    assert_strategy_safety()  # should not raise

def test_board_classifier_mainboard_reversal_blocked():
    from zmatrix.strategy.board_classifier import classify_board
    from zmatrix.strategy.b_matrix_router import is_b_matrix_search_allowed
    b = classify_board("601899")
    assert b["board_type"] == "MAINBOARD"
    r = is_b_matrix_search_allowed("MAINBOARD", "REVERSAL")
    assert r["b_matrix_search_status"] == "BLOCKED"
