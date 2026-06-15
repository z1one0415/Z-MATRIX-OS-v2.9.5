"""Tests for Board/Regime G18 Interpretation."""
from zmatrix.prediction.board_regime_interpretation import interpret_g18_action_with_board_regime
def test_mainboard_reversal_paper_track():
    r = interpret_g18_action_with_board_regime("PAPER_TRACK",0.75,{"board_type":"MAINBOARD","regime_state":"REVERSAL"})
    assert r["interpreted_as"] == "WATCH_FOR_PULLBACK_OR_CONFIRMATION"
    assert r["not_trade_signal"] is True
def test_star_momentum_paper_track():
    r = interpret_g18_action_with_board_regime("PAPER_TRACK",0.75,{"board_type":"STAR","regime_state":"MOMENTUM"})
    assert r["interpreted_as"] == "TREND_CANDIDATE_OBSERVATION"
    assert r["b_matrix_candidate_possible"] is True
