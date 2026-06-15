"""Strategy.1.1: G18 final decision integration test."""
import sys, pytest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from zmatrix.strategy.board_regime_context import build_board_regime_context

def test_mainboard_reversal_context():
    prices = [100] + [100 * (1 + d * 0.005) for d in [1,-1,1,-1,1,-1,1,-1,1,-1]*5]
    ctx = build_board_regime_context("601899", prices, "PAPER_TRACK", 0.72)
    assert ctx["board_type"] == "MAINBOARD"
    assert ctx["strategy_family"] == "REVERSAL_REPAIR"
    assert ctx["b_matrix_search_status"] == "BLOCKED"
    assert ctx["action_interpretation"]["interpreted_as"] == "WATCH_FOR_PULLBACK_OR_CONFIRMATION"
    assert ctx["not_trade_signal"] is True

def test_star_momentum_context():
    prices = [100]; v=100
    for _ in range(40): v*=1.02; prices.append(v)
    ctx = build_board_regime_context("688981", prices, "PAPER_TRACK", 0.72)
    assert ctx["board_type"] == "STAR"
    assert ctx["b_matrix_search_status"] == "ALLOWED" or ctx["b_matrix_search_status"] == "CONDITIONAL"
    assert ctx["action_interpretation"]["not_trade_signal"] is True

def test_unknown_insufficient_data():
    ctx = build_board_regime_context("999999", None, "WAIT", 0.3)
    assert ctx["board_type"] == "UNKNOWN"
    assert ctx["regime_state"] == "DATA_INSUFFICIENT"
    assert ctx["b_matrix_search_status"] == "BLOCKED"

def test_context_safety_fields():
    ctx = build_board_regime_context("601899", None, "WAIT", 0.3)
    assert ctx["alpha_claim_allowed"] is False
    assert ctx["promotion_allowed"] is False
    assert ctx["action_interpretation"]["not_trade_signal"] is True
    assert ctx["action_interpretation"]["not_alpha_claim"] is True
