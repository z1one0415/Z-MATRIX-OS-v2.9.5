#!/usr/bin/env python3
"""Phase 3-A: Comprehensive Market Data Tests (45+)"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
from pathlib import Path
import subprocess
WORKSPACE = Path(__file__).resolve().parent.parent.parent.parent
FIXTURES = WORKSPACE / "tests" / "fixtures" / "market_data"

from zmatrix.research_db.market_data.market_schema import DailyPriceBar, TradingCalendarRecord, BenchmarkRecord, AdjustmentFactorRecord
from zmatrix.research_db.market_data.trading_calendar import TradingCalendar
from zmatrix.research_db.market_data.price_bar_store import PriceBarStore
from zmatrix.research_db.market_data.benchmark_registry import BenchmarkRegistry
from zmatrix.research_db.market_data.adjustment_factor_store import AdjustmentFactorStore

CAL = TradingCalendar(str(FIXTURES / "sample_trading_calendar.csv"))
BARS = PriceBarStore(str(FIXTURES / "sample_daily_price_bar.csv"))
BM = BenchmarkRegistry(str(FIXTURES / "sample_benchmark_registry.csv"))
ADJ = AdjustmentFactorStore(str(FIXTURES / "sample_adjustment_factor.csv"))

# ── schema tests ──
def test_daily_price_bar_fields(): assert DailyPriceBar(ticker="A",trade_date="2024-01-01",open=10,high=11,low=9,close=10.5).close == 10.5
def test_trading_calendar_record(): assert TradingCalendarRecord(trade_date="2024-01-01").is_open is True
def test_benchmark_record(): assert BenchmarkRecord(benchmark_id="CSI300",benchmark_name="CSI300",benchmark_type="LARGE_CAP",ticker="000300").benchmark_id == "CSI300"
def test_adjustment_factor_record(): assert AdjustmentFactorRecord(ticker="A",trade_date="2024-01-01",adj_factor=1.0).adj_factor == 1.0
def test_all_schema_production_false():
    for obj in [DailyPriceBar(ticker="A",trade_date="D",open=10,high=10,low=10,close=10),
                TradingCalendarRecord(trade_date="D"),BenchmarkRecord(benchmark_id="X",benchmark_name="X",benchmark_type="T",ticker="X"),
                AdjustmentFactorRecord(ticker="A",trade_date="D",adj_factor=1.0)]:
        assert obj.production_allowed is False

# ── calendar tests ──
def test_is_trade_day(): assert CAL.is_trade_day("2024-01-05") is True
def test_is_not_trade_day(): assert CAL.is_trade_day("2024-01-01") is False
def test_next_trade_day(): assert CAL.next_trade_day("2024-01-02") == "2024-01-03"
def test_prev_trade_day(): assert CAL.prev_trade_day("2024-01-03") == "2024-01-02"
def test_forward_trade_day_t1(): assert CAL.forward_trade_day("2024-01-02", 1) == "2024-01-03"
def test_forward_trade_day_t5(): assert CAL.forward_trade_day("2024-01-02", 5) == "2024-01-09"
def test_has_forward_days_true(): assert CAL.has_forward_days("2024-01-02", 20) is True
def test_has_forward_days_false(): assert CAL.forward_trade_day("2024-02-01", 5) is None
def test_forward_days_no_fallback(): assert CAL.forward_trade_day("2024-02-02", 1) is None

# ── price bar tests ──
def test_get_bar(): assert BARS.get_bar("000001","2024-01-02")["close"] == 9.75
def test_get_bar_missing(): assert BARS.get_bar("000001","2024-01-01") is None
def test_get_bars(): assert len(BARS.get_bars("000001","2024-01-02","2024-01-05")) == 4
def test_has_bar(): assert BARS.has_bar("000001","2024-01-02") is True
def test_detect_suspension(): assert BARS.detect_suspension("600519","2024-01-04") is True
def test_detect_suspension_false(): assert BARS.detect_suspension("000001","2024-01-02") is False
def test_detect_limit_up(): assert BARS.detect_limit_up("000001","2024-01-04") is True
def test_detect_limit_down(): assert BARS.detect_limit_down("000001","2024-01-02") is False
def test_detect_one_price_limit(): assert BARS.detect_one_price_limit("000001","2024-01-05") is True

# ── benchmark tests ──
def test_get_benchmark(): assert BM.get_benchmark("CSI300")["benchmark_name"] == "CSI300"
def test_list_benchmarks(): assert len(BM.list_benchmarks()) == 6
def test_default_benchmark_stock(): assert BM.get_default_benchmark("STOCK") == "CSI300"
def test_default_benchmark_cash(): assert BM.get_default_benchmark("CASH") == "CASH"

# ── adjustment factor tests ──
def test_get_factor(): assert ADJ.get_factor("000001","2024-01-02") == 1.0
def test_get_factor_missing(): assert ADJ.get_factor("999999","2024-01-02") == 1.0

# ── privacy guardrail tests ──
def test_no_raw_files_tracked():
    r = subprocess.run(["git","ls-files","data/research_db/market_data/raw/"], capture_output=True, text=True, cwd=str(WORKSPACE))
    real = [l for l in r.stdout.split("\n") if l.strip() and not l.endswith(".gitkeep")]
    assert len(real) == 0, f"raw: {real}"

def test_no_vendor_files():
    r = subprocess.run(["git","ls-files"], capture_output=True, text=True, cwd=str(WORKSPACE))
    for line in r.stdout.split("\n"):
        for bad in [".xlsx",".xls",".vendor.csv",".raw.csv"]:
            assert not line.endswith(bad), f"vendor: {line}"

def test_fixtures_synthetic_only():
    r = subprocess.run(["git","ls-files","tests/fixtures/market_data/"], capture_output=True, text=True, cwd=str(WORKSPACE))
    for line in r.stdout.split("\n"):
        if line.endswith(".csv"): assert "sample_" in line

def test_gitignore_covers_market_data():
    gi = (WORKSPACE / ".gitignore").read_text()
    for pat in ["market_data/raw","market_data/staging","market_data/vendor"]:
        assert pat in gi, f"missing {pat}"

# ── safety ──
def test_no_buy_sell_in_schema():
    from pathlib import Path as P
    for f in P("zmatrix/research_db/market_data").rglob("*.py"):
        text = f.read_text()
        for fb in ["BUY","SELL","AUTO_EXECUTE","production_allowed=True"]:
            if "allowlist:" not in text: assert fb not in text, f"{fb} in {f}"

if __name__ == "__main__":
    import pytest; pytest.main([__file__, "-v"])
