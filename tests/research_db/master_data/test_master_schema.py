#!/usr/bin/env python3
"""Phase 2-A: Master Data Schema Tests — enums, dataclass creation, default values."""
from __future__ import annotations

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

from zmatrix.research_db.master_data import (
    Exchange, ListingStatus, AliasType, Confidence,
    SecurityMaster, TickerAlias, IndustryMapping,
    SectorMapping, ChainTaxonomy, ChainNodeMapping,
)


def test_exchange_enum_values():
    assert Exchange.SSE.value == "SSE"
    assert Exchange.SZSE.value == "SZSE"
    assert Exchange.BSE.value == "BSE"
    assert len(Exchange) == 3


def test_listing_status_enum_values():
    assert ListingStatus.LISTED.value == "LISTED"
    assert ListingStatus.DELISTED.value == "DELISTED"
    assert ListingStatus.SUSPENDED.value == "SUSPENDED"
    assert ListingStatus.UNKNOWN.value == "UNKNOWN"
    assert len(ListingStatus) == 4


def test_alias_type_enum_values():
    assert AliasType.FORMER_NAME.value == "FORMER_NAME"
    assert AliasType.SHORT_NAME.value == "SHORT_NAME"
    assert AliasType.ENGLISH_NAME.value == "ENGLISH_NAME"
    assert AliasType.CODE_CHANGE.value == "CODE_CHANGE"
    assert len(AliasType) == 4


def test_confidence_enum_values():
    assert Confidence.HIGH.value == "HIGH"
    assert Confidence.MEDIUM.value == "MEDIUM"
    assert Confidence.LOW.value == "LOW"
    assert Confidence.UNVERIFIED.value == "UNVERIFIED"
    assert len(Confidence) == 4


def test_security_master_creation():
    sm = SecurityMaster(
        ticker="600519",
        name="贵州茅台",
        exchange=Exchange.SSE,
        listing_date="2001-08-27",
        listing_status=ListingStatus.LISTED,
        market_cap_float=2100000000000.0,
        market_cap_total=2100000000000.0,
        sw_l1="食品饮料",
        sw_l2="白酒Ⅱ",
        sw_l3="白酒Ⅲ",
    )
    assert sm.ticker == "600519"
    assert sm.name == "贵州茅台"
    assert sm.exchange == Exchange.SSE
    assert sm.sw_l1 == "食品饮料"
    assert sm.production_allowed is False


def test_security_master_defaults():
    sm = SecurityMaster(ticker="000001", name="平安银行", exchange=Exchange.SZSE)
    assert sm.listing_date is None
    assert sm.listing_status == ListingStatus.UNKNOWN
    assert sm.market_cap_float is None
    assert sm.market_cap_total is None
    assert sm.sw_l1 is None
    assert sm.sw_l2 is None
    assert sm.sw_l3 is None
    assert sm.production_allowed is False
    assert sm.listing_status is not None and isinstance(sm.listing_status, ListingStatus)


def test_ticker_alias_creation():
    ta = TickerAlias(
        ticker="600519",
        alias="茅台",
        alias_type=AliasType.SHORT_NAME,
        effective_date="2001-08-27",
    )
    assert ta.ticker == "600519"
    assert ta.alias == "茅台"
    assert ta.alias_type == AliasType.SHORT_NAME
    assert ta.expiry_date is None
    assert ta.production_allowed is False


def test_industry_mapping_creation():
    im = IndustryMapping(
        ticker="600519",
        sw_l1="食品饮料",
        sw_l2="白酒Ⅱ",
        sw_l3="白酒Ⅲ",
        confidence=Confidence.HIGH,
    )
    assert im.ticker == "600519"
    assert im.sw_l1 == "食品饮料"
    assert im.sw_l3 == "白酒Ⅲ"
    assert im.confidence == Confidence.HIGH
    assert im.production_allowed is False


def test_industry_mapping_defaults():
    im = IndustryMapping(ticker="000001")
    assert im.sw_l1 is None
    assert im.sw_l2 is None
    assert im.sw_l3 is None
    assert im.confidence == Confidence.UNVERIFIED
    assert im.production_allowed is False


def test_sector_mapping_creation():
    sm = SectorMapping(ticker="002472", sector_id="SW801880", sector_name="汽车", weight=0.8)
    assert sm.ticker == "002472"
    assert sm.sector_id == "SW801880"
    assert sm.sector_name == "汽车"
    assert sm.weight == 0.8
    assert sm.production_allowed is False


def test_chain_taxonomy_creation():
    ct = ChainTaxonomy(chain_id="CHN001", chain_name="人形机器人链", chain_type="MANUFACTURING")
    assert ct.chain_id == "CHN001"
    assert ct.chain_name == "人形机器人链"
    assert ct.chain_type == "MANUFACTURING"
    assert ct.parent_chain_id is None
    assert ct.production_allowed is False


def test_chain_taxonomy_with_parent():
    ct = ChainTaxonomy(
        chain_id="CHN004",
        chain_name="减速器子链",
        chain_type="MANUFACTURING",
        parent_chain_id="CHN001",
    )
    assert ct.parent_chain_id == "CHN001"
    assert ct.production_allowed is False


def test_chain_node_mapping_creation():
    cnm = ChainNodeMapping(
        ticker="002472",
        chain_id="CHN001",
        chain_layer="HARDWARE_BOTTLENECK",
        chain_position="precision_reducer",
        value_capture_grade="B",
        evidence_grade="A",
    )
    assert cnm.ticker == "002472"
    assert cnm.chain_id == "CHN001"
    assert cnm.chain_layer == "HARDWARE_BOTTLENECK"
    assert cnm.chain_position == "precision_reducer"
    assert cnm.value_capture_grade == "B"
    assert cnm.evidence_grade == "A"
    assert cnm.production_allowed is False


def test_all_dataclasses_have_production_false():
    sm = SecurityMaster(ticker="000001", name="test", exchange=Exchange.SZSE)
    ta = TickerAlias(ticker="000001", alias="t", alias_type=AliasType.SHORT_NAME)
    im = IndustryMapping(ticker="000001")
    sem = SectorMapping(ticker="000001", sector_id="S1", sector_name="n", weight=1.0)
    ct = ChainTaxonomy(chain_id="C1", chain_name="n", chain_type="t")
    cnm = ChainNodeMapping(ticker="000001", chain_id="C1", chain_layer="L1", chain_position="P1", value_capture_grade="C", evidence_grade="B")
    objs = [sm, ta, im, sem, ct, cnm]
    for obj in objs:
        assert getattr(obj, "production_allowed") is False, f"{type(obj).__name__} has production_allowed != False"


def test_enum_membership():
    assert Exchange("SSE") == Exchange.SSE
    assert Exchange("SZSE") == Exchange.SZSE
    assert ListingStatus("LISTED") == ListingStatus.LISTED
    assert AliasType("FORMER_NAME") == AliasType.FORMER_NAME
    assert Confidence("LOW") == Confidence.LOW


def test_no_buy_sell_tokens_in_schema():
    import inspect
    from pathlib import Path
    src = Path(__file__).resolve().parent.parent.parent.parent / "zmatrix" / "research_db" / "master_data" / "__init__.py"
    text = src.read_text()
    forbidden = ["BUY", "SELL", "STRONG_BUY", "AUTO_BUY", "AUTO_SELL",
                 "BROKER_ORDER", "PLACE_ORDER", "SEND_ORDER", "EXECUTE_TRADE",
                 "PRODUCTION_READY", "REAL_TRADE_READY"]
    for token in forbidden:
        assert token not in text, f"Forbidden token '{token}' found in master_data/__init__.py"


def test_no_production_flag_set_to_true():
    from pathlib import Path
    src = Path(__file__).resolve().parent.parent.parent.parent / "zmatrix" / "research_db" / "master_data" / "__init__.py"
    text = src.read_text()
    for token in [
        "real_trade_allowed=True",
        "broker_order_allowed=True",
        "runtime_enabled=True",
        "auto_buy_allowed=True",
        "auto_sell_allowed=True",
        "production_allowed=True",
    ]:
        assert token not in text, f"Forbidden production flag {token} in master_data/__init__.py"


if __name__ == "__main__":
    test_exchange_enum_values()
    test_listing_status_enum_values()
    test_alias_type_enum_values()
    test_confidence_enum_values()
    test_security_master_creation()
    test_security_master_defaults()
    test_ticker_alias_creation()
    test_industry_mapping_creation()
    test_industry_mapping_defaults()
    test_sector_mapping_creation()
    test_chain_taxonomy_creation()
    test_chain_taxonomy_with_parent()
    test_chain_node_mapping_creation()
    test_all_dataclasses_have_production_false()
    test_enum_membership()
    test_no_buy_sell_tokens_in_schema()
    test_no_production_flag_set_to_true()
    print("✅ Phase 2-A Master Data Schema tests PASS")
