#!/usr/bin/env python3
"""Phase 2-C: Industry/Sector Mapping Tests."""
from __future__ import annotations

import sys
import os
from datetime import date
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

from zmatrix.research_db.master_data.industry_taxonomy import IndustryTaxonomy
from zmatrix.research_db.master_data.sector_mapper import SectorMapper

FIXTURE_DIR = Path(__file__).resolve().parent.parent.parent / "fixtures" / "master_data"
INDUSTRY_CSV = str(FIXTURE_DIR / "sample_industry_mapping.csv")
SECTOR_CSV = str(FIXTURE_DIR / "sample_sector_mapping.csv")


# ── IndustryTaxonomy Tests ──

def test_industry_loads_all():
    tax = IndustryTaxonomy(INDUSTRY_CSV)
    assert len(tax._all) == 5


def test_industry_get_industry():
    tax = IndustryTaxonomy(INDUSTRY_CSV)
    result = tax.get_industry("600519")
    assert result["ticker"] == "600519"
    assert result["sw_l1"] == "食品饮料"
    assert result["sw_l2"] == "白酒Ⅱ"
    assert result["sw_l3"] == "白酒Ⅲ"
    assert result["confidence"] == "HIGH"


def test_industry_get_industry_not_found():
    tax = IndustryTaxonomy(INDUSTRY_CSV)
    try:
        tax.get_industry("999999")
        assert False, "expected KeyError"
    except KeyError:
        pass


def test_industry_get_tickers_in_industry():
    tax = IndustryTaxonomy(INDUSTRY_CSV)
    tickers = tax.get_tickers_in_industry("汽车")
    assert tickers == ["002472"]


def test_industry_get_tickers_empty():
    tax = IndustryTaxonomy(INDUSTRY_CSV)
    tickers = tax.get_tickers_in_industry("国防军工")
    assert tickers == []


def test_industry_list_industries():
    tax = IndustryTaxonomy(INDUSTRY_CSV)
    inds = tax.list_industries()
    assert "电力设备" in inds
    assert "电子" in inds
    assert "汽车" in inds
    assert "食品饮料" in inds
    assert "银行" in inds


def test_industry_count_by_industry():
    tax = IndustryTaxonomy(INDUSTRY_CSV)
    counts = tax.count_by_industry()
    assert counts["食品饮料"] == 1
    assert counts["银行"] == 1
    assert counts["汽车"] == 1
    assert counts["电力设备"] == 1
    assert counts["电子"] == 1


def test_industry_detect_low_confidence():
    tax = IndustryTaxonomy(INDUSTRY_CSV)
    assert tax.detect_low_confidence("600519") is False
    assert tax.detect_low_confidence("002472") is False


def test_industry_detect_low_confidence_missing():
    tax = IndustryTaxonomy(INDUSTRY_CSV)
    assert tax.detect_low_confidence("999999") is True


def test_industry_detect_missing():
    tax = IndustryTaxonomy(INDUSTRY_CSV)
    assert tax.detect_missing("600519") is False
    assert tax.detect_missing("999999") is True


def test_industry_detect_expired():
    tax = IndustryTaxonomy(INDUSTRY_CSV)
    assert tax.detect_expired("600519", date(2026, 5, 30)) is False
    assert tax.detect_expired("999999", date(2026, 5, 30)) is True


# ── SectorMapper Tests ──

def test_sector_loads_all():
    sm = SectorMapper(SECTOR_CSV)
    assert len(sm._all) == 5


def test_sector_get_sectors():
    sm = SectorMapper(SECTOR_CSV)
    sectors = sm.get_sectors("600519")
    assert len(sectors) == 1
    assert sectors[0]["sector_id"] == "SW801120"
    assert sectors[0]["sector_name"] == "食品饮料"
    assert sectors[0]["weight"] == 1.0


def test_sector_get_sectors_empty():
    sm = SectorMapper(SECTOR_CSV)
    sectors = sm.get_sectors("999999")
    assert sectors == []


def test_sector_get_tickers_in_sector():
    sm = SectorMapper(SECTOR_CSV)
    tickers = sm.get_tickers_in_sector("SW801880")
    assert tickers == ["002472"]


def test_sector_list_sectors():
    sm = SectorMapper(SECTOR_CSV)
    sectors = sm.list_sectors()
    assert "SW801080" in sectors
    assert "SW801120" in sectors
    assert "SW801730" in sectors
    assert "SW801750" in sectors
    assert "SW801880" in sectors


def test_sector_detect_speculative_theme():
    sm = SectorMapper(SECTOR_CSV)
    assert sm.detect_speculative_theme("600519") is False
    assert sm.detect_speculative_theme("000001") is False


def test_sector_detect_missing_sector():
    sm = SectorMapper(SECTOR_CSV)
    assert sm.detect_missing_sector("600519") is False
    assert sm.detect_missing_sector("999999") is True


def test_all_production_allowed_false():
    tax = IndustryTaxonomy(INDUSTRY_CSV)
    sm = SectorMapper(SECTOR_CSV)
    for im in tax._all:
        assert im.production_allowed is False
    for sec in sm._all:
        assert sec.production_allowed is False


if __name__ == "__main__":
    test_industry_loads_all()
    test_industry_get_industry()
    test_industry_get_industry_not_found()
    test_industry_get_tickers_in_industry()
    test_industry_get_tickers_empty()
    test_industry_list_industries()
    test_industry_count_by_industry()
    test_industry_detect_low_confidence()
    test_industry_detect_low_confidence_missing()
    test_industry_detect_missing()
    test_industry_detect_expired()
    test_sector_loads_all()
    test_sector_get_sectors()
    test_sector_get_sectors_empty()
    test_sector_get_tickers_in_sector()
    test_sector_list_sectors()
    test_sector_detect_speculative_theme()
    test_sector_detect_missing_sector()
    test_all_production_allowed_false()
    print("✅ Phase 2-C Industry/Sector Mapping tests PASS")
