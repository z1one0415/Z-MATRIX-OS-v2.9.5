#!/usr/bin/env python3
"""Phase 3-A.1: Depth Gate Tests — T20/T60 strictness + edge cases (14 tests)"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
from pathlib import Path
import csv
WORKSPACE = Path(__file__).resolve().parent.parent.parent.parent
FIXTURES = WORKSPACE / "tests" / "fixtures" / "market_data"

from zmatrix.research_db.market_data.trading_calendar import TradingCalendar
from zmatrix.research_db.market_data.price_bar_store import PriceBarStore
from zmatrix.research_db.market_data.benchmark_registry import BenchmarkRegistry
from zmatrix.research_db.market_data.adjustment_factor_store import AdjustmentFactorStore
from zmatrix.research_db.market_data.market_schema import DailyPriceBar, TradingCalendarRecord, BenchmarkRecord, AdjustmentFactorRecord

CAL = TradingCalendar(str(FIXTURES / "sample_trading_calendar.csv"))

def test_depth_t20_forward_sufficient():
    d = CAL.forward_trade_day("2024-01-02", 20)
    assert d is not None, "T20 should have sufficient forward days"
    assert d >= "2024-01-29"

def test_depth_t20_forward_insufficient():
    d = CAL.forward_trade_day("2024-02-02", 20)
    assert d is None, "T20 insufficient must return None"

def test_depth_t60_has_forward_false():
    assert CAL.has_forward_days("2024-01-31", 60) is False

def test_depth_next_trade_for_non_trade_day():
    d = CAL.next_trade_day("2024-01-01")
    assert d == "2024-01-02", f"next after non-trade-day should be 2024-01-02, got {d}"

def test_depth_prev_trade_for_non_trade_day():
    d = CAL.prev_trade_day("2024-01-06")
    assert d == "2024-01-05", f"prev before non-trade-day should be 2024-01-05, got {d}"

def test_depth_suspended_bar_not_normal():
    BARS = PriceBarStore(str(FIXTURES / "sample_daily_price_bar.csv"))
    assert BARS.detect_suspension("600519","2024-01-04") is True
    bar = BARS.get_bar("600519","2024-01-04")
    assert bar is not None

def test_depth_one_price_limit_detection():
    BARS = PriceBarStore(str(FIXTURES / "sample_daily_price_bar.csv"))
    assert BARS.detect_one_price_limit("000001","2024-01-05") is True

def test_depth_benchmark_default_stock_to_major_index():
    BM = BenchmarkRegistry(str(FIXTURES / "sample_benchmark_registry.csv"))
    d = BM.get_default_benchmark("STOCK")
    assert d in ("CSI300","CSI500"), f"default stock benchmark: {d}"

def test_depth_benchmark_default_cash_to_cash():
    BM = BenchmarkRegistry(str(FIXTURES / "sample_benchmark_registry.csv"))
    assert BM.get_default_benchmark("CASH") == "CASH"

def test_depth_adjustment_factor_missing_returns_one():
    ADJ = AdjustmentFactorStore(str(FIXTURES / "sample_adjustment_factor.csv"))
    assert ADJ.get_factor("999999","2024-01-02") == 1.0

def test_depth_fixtures_are_synthetic_only():
    for fixture_name in ["sample_trading_calendar.csv","sample_daily_price_bar.csv","sample_benchmark_registry.csv","sample_adjustment_factor.csv"]:
        with open(FIXTURES / fixture_name, newline="") as f:
            for row in csv.DictReader(f):
                ds = row.get("data_status","")
                assert ds != "VENDOR_EXPORT", f"vendor data in {fixture_name}"
                assert ds != "BROKER_EXPORT", f"broker data in {fixture_name}"

def test_depth_production_allowed_forced_false():
    bar = DailyPriceBar(ticker="X",trade_date="D",open=10,high=10,low=10,close=10,production_allowed=True)
    assert bar.production_allowed is False
    cal = TradingCalendarRecord(trade_date="D",production_allowed=True)
    assert cal.production_allowed is False

def test_depth_no_outcome_function_names_in_market_data():
    for py_file in (WORKSPACE / "zmatrix" / "research_db" / "market_data").rglob("*.py"):
        text = py_file.read_text()
        for fn in ["compute_outcome","calculate_return","alpha","benchmark_alpha","t20_outcome","t60_outcome"]:
            assert fn not in text, f"{fn} in {py_file.name} (outcome should not be in P3-A)"

def test_depth_has_forward_t1_even_at_boundary():
    assert CAL.has_forward_days("2024-02-01", 1) is True

if __name__ == "__main__":
    import pytest; pytest.main([__file__, "-v"])
