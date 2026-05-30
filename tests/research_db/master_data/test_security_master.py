#!/usr/bin/env python3
"""Phase 2-B: SecurityMasterRegistry Tests."""
from __future__ import annotations

import sys
import os
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

from zmatrix.research_db.master_data import Exchange, ListingStatus
from zmatrix.research_db.master_data.security_master import SecurityMasterRegistry

FIXTURE_DIR = Path(__file__).resolve().parent.parent.parent / "fixtures" / "master_data"
SAMPLE_CSV = str(FIXTURE_DIR / "sample_security_master.csv")


def test_registry_loads_all_tickers():
    reg = SecurityMasterRegistry(SAMPLE_CSV)
    assert reg.count() == 5


def test_get_by_ticker_found():
    reg = SecurityMasterRegistry(SAMPLE_CSV)
    sm = reg.get_by_ticker("600519")
    assert sm.name == "贵州茅台"
    assert sm.exchange == Exchange.SSE


def test_get_by_ticker_not_found_raises():
    reg = SecurityMasterRegistry(SAMPLE_CSV)
    try:
        reg.get_by_ticker("999999")
        assert False, "expected KeyError"
    except KeyError:
        pass


def test_has_ticker():
    reg = SecurityMasterRegistry(SAMPLE_CSV)
    assert reg.has_ticker("600519") is True
    assert reg.has_ticker("999999") is False


def test_get_by_name():
    reg = SecurityMasterRegistry(SAMPLE_CSV)
    results = reg.get_by_name("贵州茅台")
    assert len(results) == 1
    assert results[0].ticker == "600519"


def test_get_by_name_not_found():
    reg = SecurityMasterRegistry(SAMPLE_CSV)
    assert reg.get_by_name("不存在") == []


def test_get_by_exchange():
    reg = SecurityMasterRegistry(SAMPLE_CSV)
    sse = reg.get_by_exchange("SSE")
    assert len(sse) == 2
    tickers = {sm.ticker for sm in sse}
    assert tickers == {"600519", "688981"}


def test_get_by_industry():
    reg = SecurityMasterRegistry(SAMPLE_CSV)
    auto = reg.get_by_industry("汽车")
    assert len(auto) == 1
    assert auto[0].ticker == "002472"


def test_get_by_industry_not_found():
    reg = SecurityMasterRegistry(SAMPLE_CSV)
    assert reg.get_by_industry("国防军工") == []


def test_list_all():
    reg = SecurityMasterRegistry(SAMPLE_CSV)
    all_sm = reg.list_all()
    assert len(all_sm) == 5
    tickers = {sm.ticker for sm in all_sm}
    assert tickers == {"600519", "000001", "002472", "300750", "688981"}


def test_count():
    reg = SecurityMasterRegistry(SAMPLE_CSV)
    assert reg.count() == 5


def test_all_production_allowed_false():
    reg = SecurityMasterRegistry(SAMPLE_CSV)
    for sm in reg.list_all():
        assert sm.production_allowed is False


def test_get_by_name_multiple():
    reg = SecurityMasterRegistry(SAMPLE_CSV)
    empty = reg.get_by_name("")
    assert empty == []


if __name__ == "__main__":
    test_registry_loads_all_tickers()
    test_get_by_ticker_found()
    test_get_by_ticker_not_found_raises()
    test_has_ticker()
    test_get_by_name()
    test_get_by_name_not_found()
    test_get_by_exchange()
    test_get_by_industry()
    test_get_by_industry_not_found()
    test_list_all()
    test_count()
    test_all_production_allowed_false()
    test_get_by_name_multiple()
    print("✅ Phase 2-B SecurityMasterRegistry tests PASS")
