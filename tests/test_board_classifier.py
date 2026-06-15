"""Tests for Board Classifier."""
from zmatrix.strategy.board_classifier import classify_board
def test_star(): assert classify_board("688981")["board_type"] == "STAR"
def test_chinext(): assert classify_board("300750")["board_type"] == "CHINEXT"
def test_mainboard(): assert classify_board("000977")["board_type"] == "MAINBOARD"
def test_mainboard_600(): assert classify_board("601899")["board_type"] == "MAINBOARD"
def test_sme(): assert classify_board("002472")["board_type"] == "SME"
def test_unknown(): assert classify_board("999999")["board_type"] == "UNKNOWN"
