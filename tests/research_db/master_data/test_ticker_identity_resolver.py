#!/usr/bin/env python3
"""Phase 2-B: Ticker Identity Resolver Tests."""
from __future__ import annotations

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

from zmatrix.research_db.master_data.ticker_identity_resolver import (
    normalize_ticker,
    resolve_identity,
)


def test_normalize_strips_whitespace():
    assert normalize_ticker("  600519  ") == "600519.SH"


def test_normalize_uppercase():
    assert normalize_ticker("688981.sh") == "688981.SH"


def test_normalize_removes_special_chars():
    assert normalize_ticker("600-519") == "600519.SH"


def test_normalize_appends_sh_suffix():
    assert normalize_ticker("600519") == "600519.SH"


def test_normalize_appends_sz_suffix():
    assert normalize_ticker("000001") == "000001.SZ"


def test_normalize_appends_bj_suffix():
    assert normalize_ticker("830001") == "830001.BJ"


def test_normalize_preserves_existing_suffix():
    assert normalize_ticker("600519.SH") == "600519.SH"


def test_normalize_szse_chinext():
    assert normalize_ticker("300750") == "300750.SZ"


def test_normalize_sse_star():
    assert normalize_ticker("688981") == "688981.SH"


def test_resolve_identity_sse():
    result = resolve_identity("600519")
    assert result["canonical_ticker"] == "600519.SH"
    assert result["exchange"] == "SSE"
    assert result["display_name"] == "600519"
    assert result["status"] == "ACTIVE"


def test_resolve_identity_szse():
    result = resolve_identity("000001")
    assert result["canonical_ticker"] == "000001.SZ"
    assert result["exchange"] == "SZSE"


def test_resolve_identity_bse():
    result = resolve_identity("830001")
    assert result["canonical_ticker"] == "830001.BJ"
    assert result["exchange"] == "BSE"


def test_resolve_identity_with_aliases():
    aliases = {"600519": "MOUTAI.SH"}
    result = resolve_identity("600519", aliases=aliases)
    assert result["canonical_ticker"] == "MOUTAI.SH"


def test_normalize_unknown_prefix_no_suffix():
    assert normalize_ticker("ABC123") == "ABC123"


def test_resolve_identity_unknown_prefix():
    result = resolve_identity("ABC123")
    assert result["exchange"] is None


if __name__ == "__main__":
    test_normalize_strips_whitespace()
    test_normalize_uppercase()
    test_normalize_removes_special_chars()
    test_normalize_appends_sh_suffix()
    test_normalize_appends_sz_suffix()
    test_normalize_appends_bj_suffix()
    test_normalize_preserves_existing_suffix()
    test_normalize_szse_chinext()
    test_normalize_sse_star()
    test_resolve_identity_sse()
    test_resolve_identity_szse()
    test_resolve_identity_bse()
    test_resolve_identity_with_aliases()
    test_normalize_unknown_prefix_no_suffix()
    test_resolve_identity_unknown_prefix()
    print("✅ Phase 2-B Ticker Identity Resolver tests PASS")
