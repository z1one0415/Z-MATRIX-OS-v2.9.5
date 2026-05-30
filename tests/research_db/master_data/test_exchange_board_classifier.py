#!/usr/bin/env python3
"""Phase 2-B: Exchange Board Classifier Tests."""
from __future__ import annotations

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

from zmatrix.research_db.master_data import Exchange
from zmatrix.research_db.master_data.exchange_board_classifier import (
    classify_exchange,
    detect_board,
    is_ticker_format_valid,
)


def test_classify_sse_main():
    assert classify_exchange("600519") == Exchange.SSE
    assert classify_exchange("601318") == Exchange.SSE
    assert classify_exchange("603259") == Exchange.SSE


def test_classify_sse_star():
    assert classify_exchange("688981") == Exchange.SSE
    assert classify_exchange("688981.SH") == Exchange.SSE


def test_classify_szse_main():
    assert classify_exchange("000001") == Exchange.SZSE
    assert classify_exchange("002472") == Exchange.SZSE


def test_classify_szse_chinext():
    assert classify_exchange("300750") == Exchange.SZSE
    assert classify_exchange("301000") == Exchange.SZSE


def test_classify_bse():
    assert classify_exchange("830001") == Exchange.BSE
    assert classify_exchange("430001") == Exchange.BSE


def test_classify_invalid():
    assert classify_exchange("999999") is None
    assert classify_exchange("ABC") is None


def test_detect_board_main():
    assert detect_board("600519") == "MAIN"
    assert detect_board("000001") == "MAIN"


def test_detect_board_star():
    assert detect_board("688981") == "STAR"


def test_detect_board_chinext():
    assert detect_board("300750") == "CHINEXT"


def test_detect_board_bse():
    assert detect_board("830001") == "BSE"


def test_detect_board_invalid():
    assert detect_board("999999") is None
    assert detect_board("") is None


def test_is_ticker_format_valid_sse():
    assert is_ticker_format_valid("600519") is True
    assert is_ticker_format_valid("688981") is True


def test_is_ticker_format_valid_szse():
    assert is_ticker_format_valid("000001") is True
    assert is_ticker_format_valid("300750") is True


def test_is_ticker_format_valid_bse():
    assert is_ticker_format_valid("830001") is True


def test_is_ticker_format_valid_with_suffix():
    assert is_ticker_format_valid("600519.SH") is True


def test_is_ticker_format_valid_invalid():
    assert is_ticker_format_valid("999999") is False
    assert is_ticker_format_valid("ABC") is False
    assert is_ticker_format_valid("12") is False
    assert is_ticker_format_valid("") is False
    assert is_ticker_format_valid("600-519") is False


if __name__ == "__main__":
    test_classify_sse_main()
    test_classify_sse_star()
    test_classify_szse_main()
    test_classify_szse_chinext()
    test_classify_bse()
    test_classify_invalid()
    test_detect_board_main()
    test_detect_board_star()
    test_detect_board_chinext()
    test_detect_board_bse()
    test_detect_board_invalid()
    test_is_ticker_format_valid_sse()
    test_is_ticker_format_valid_szse()
    test_is_ticker_format_valid_bse()
    test_is_ticker_format_valid_with_suffix()
    test_is_ticker_format_valid_invalid()
    print("✅ Phase 2-B Exchange Board Classifier tests PASS")
