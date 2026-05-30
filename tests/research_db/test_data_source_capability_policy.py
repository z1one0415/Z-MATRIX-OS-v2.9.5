#!/usr/bin/env python3
"""ResearchDB Phase 0: Data Source Capability Tests"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from zmatrix.research_db.data_source_capability import DEFAULT_SOURCE_REGISTRY, DataSourceCapability


def test_registry_minimum_sources():
    assert len(DEFAULT_SOURCE_REGISTRY) >= 8


def test_all_sources_have_production_false():
    for name, cap in DEFAULT_SOURCE_REGISTRY.items():
        assert cap.usable_for_production is False, f"{name} has usable_for_production=True"


def test_manual_trade_import_can_backtest():
    src = DEFAULT_SOURCE_REGISTRY["manual_trade_import"]
    assert src.usable_for_backtest is True
    assert src.usable_for_production is False


def test_financial_snapshot_cannot_backtest():
    src = DEFAULT_SOURCE_REGISTRY["financial_current_snapshot"]
    assert src.usable_for_backtest is False
    assert src.usable_for_current_snapshot is True


def test_daily_price_pit_safe():
    src = DEFAULT_SOURCE_REGISTRY["daily_price_csv"]
    assert src.pit_safe is True


if __name__ == "__main__":
    test_registry_minimum_sources()
    test_all_sources_have_production_false()
    test_manual_trade_import_can_backtest()
    test_financial_snapshot_cannot_backtest()
    test_daily_price_pit_safe()
    print("✅ ResearchDB Phase 0 Data Source Capability tests PASS")
