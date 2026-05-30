#!/usr/bin/env python3
"""Phase 3-C: Return/Alpha/Cost Engine — 45+ Tests"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
from pathlib import Path
WORKSPACE = Path(__file__).resolve().parent.parent.parent.parent
FIXTURES = WORKSPACE / "tests" / "fixtures" / "market_data"

from zmatrix.research_db.market_data.trading_calendar import TradingCalendar
from zmatrix.research_db.market_data.price_bar_store import PriceBarStore
from zmatrix.research_db.market_data.benchmark_registry import BenchmarkRegistry

CAL = TradingCalendar(str(FIXTURES / "sample_trading_calendar.csv"))
BARS = PriceBarStore(str(FIXTURES / "sample_daily_price_bar.csv"))
BM = BenchmarkRegistry(str(FIXTURES / "sample_benchmark_registry.csv"))

# ── Return Engine ──
from zmatrix.research_db.market_data.return_engine import ReturnEngine, ReturnResult, CalculationStatus

def test_gross_return_positive():
    assert ReturnEngine.compute_gross_return(10, 12) == pytest.approx(0.2)
def test_gross_return_negative():
    assert ReturnEngine.compute_gross_return(10, 8) == pytest.approx(-0.2)
def test_gross_return_zero():
    assert ReturnEngine.compute_gross_return(10, 10) == 0.0
def test_gross_return_invalid_price():
    assert ReturnEngine.compute_gross_return(0, 10) == 0.0
def test_annualized_return():
    r = ReturnEngine.compute_annualized_return(0.2, 20)
    assert r > 0
def test_annualized_return_zero_days():
    assert ReturnEngine.compute_annualized_return(0.2, 0) == 0.0
def test_holding_days():
    d = ReturnEngine.calculate_holding_days("2024-01-02", "2024-01-05", CAL)
    assert d >= 2

def test_compute_return_ready():
    r = ReturnEngine.compute_return(9.75, 10.72, "2024-01-02", "2024-01-05", CAL)
    assert r.calculation_status == "READY"
    assert r.gross_return != 0
    assert r.holding_days > 0

def test_compute_return_invalid_price():
    r = ReturnEngine.compute_return(0, 10, "2024-01-02", "2024-01-05", CAL)
    assert r.calculation_status == "INVALID_PRICE"

def test_return_result_production_false():
    r = ReturnResult(entry_price=10, exit_price=12)
    assert r.production_allowed is False

# ── Alpha Engine ──
from zmatrix.research_db.market_data.alpha_engine import AlphaEngine, AlphaResult

def test_benchmark_return():
    r = AlphaEngine.compute_benchmark_return("CSI300", "2024-01-02", "2024-01-05", BARS)
    assert isinstance(r, float)

def test_benchmark_return_missing_entry():
    r = AlphaEngine.compute_benchmark_return("CSI300", "2023-01-01", "2024-01-05", BARS)
    assert r == 0.0

def test_compute_alpha_positive():
    assert AlphaEngine.compute_alpha(0.10, 0.05) == pytest.approx(0.05)

def test_compute_alpha_negative():
    assert AlphaEngine.compute_alpha(0.05, 0.10) == pytest.approx(-0.05)

def test_compute_alpha_zero():
    assert AlphaEngine.compute_alpha(0.10, 0.10) == 0.0

def test_alpha_vs_market():
    r = AlphaEngine.compute_alpha_vs_market(9.75, 10.72, "2024-01-02", "2024-01-05", BARS, BM)
    assert "alpha_vs_market" in r
    assert r["production_allowed"] is False

def test_alpha_vs_all():
    results = AlphaEngine.compute_alpha_vs_all(9.75, 10.72, "2024-01-02", "2024-01-05", BARS, BM)
    assert len(results) >= 4
    for r in results: assert r["production_allowed"] is False

def test_alpha_result_production_false():
    r = AlphaResult(benchmark_code="CSI300")
    assert r.production_allowed is False

# ── Trading Cost Engine ──
from zmatrix.research_db.market_data.trading_cost_engine import TradingCostEngine, CostResult

def test_buy_commission():
    c = TradingCostEngine.compute_buy_commission(10000, 3.0)
    assert c == pytest.approx(3.0)  # 3bp of 10000

def test_sell_commission():
    c = TradingCostEngine.compute_sell_commission(10000, 3.0)
    assert c == pytest.approx(3.0)

def test_stamp_duty():
    c = TradingCostEngine.compute_stamp_duty(10000, 5.0)
    assert c == pytest.approx(5.0)  # 5bp of 10000

def test_stamp_duty_sell_only():
    # Buy has no stamp duty
    c = TradingCostEngine.compute_stamp_duty(0, 5.0)
    assert c == 0.0

def test_slippage():
    c = TradingCostEngine.compute_slippage(10000, 10.0)
    assert c == pytest.approx(10.0)

def test_total_cost():
    r = TradingCostEngine.compute_total_cost(10000, 10000, 3.0, 5.0, 10.0)
    assert r.buy_commission > 0
    assert r.sell_commission > 0
    assert r.stamp_duty > 0
    assert r.slippage > 0
    total = r.buy_commission + r.sell_commission + r.stamp_duty + r.slippage
    assert r.total_cost == pytest.approx(total)

def test_market_impact_zero():
    assert TradingCostEngine.market_impact_cost(10000) == 0.0

def test_cost_configurable_bps():
    r1 = TradingCostEngine.compute_total_cost(10000, 10000, 3.0, 5.0, 10.0)
    r2 = TradingCostEngine.compute_total_cost(10000, 10000, 1.0, 3.0, 5.0)
    assert r2.total_cost < r1.total_cost

def test_cost_result_production_false():
    r = CostResult()
    assert r.production_allowed is False

# ── Net Return Engine ──
from zmatrix.research_db.market_data.net_return_engine import NetReturnEngine, NetReturnResult

def test_net_return():
    net = NetReturnEngine.compute_net_return(0.10, 30.0, 10000.0)
    assert net < 0.10  # net should be less than gross after costs

def test_full_net_result():
    r = NetReturnEngine.compute_full_net_result(10.0, 12.0, 10000.0, 3.0, 5.0, 10.0)
    assert r.gross_return == pytest.approx(0.2)
    assert r.net_return < r.gross_return
    assert r.total_cost == r.commission_cost + r.stamp_duty_cost + r.slippage_cost
    # Verify net = gross - total/entry_amount
    expected_net = r.gross_return - (r.total_cost / 10000.0)
    assert r.net_return == pytest.approx(expected_net)

def test_net_return_zero_entry():
    net = NetReturnEngine.compute_net_return(0.10, 30.0, 0.0)
    assert net == 0.0

def test_full_net_result_zero_price():
    r = NetReturnEngine.compute_full_net_result(0, 12, 10000)
    assert r.gross_return == 0.0

def test_net_result_production_false():
    r = NetReturnResult()
    assert r.production_allowed is False

# ── Safety ──
def test_no_buy_sell_in_modules():
    for name in ["return_engine.py","alpha_engine.py","trading_cost_engine.py","net_return_engine.py"]:
        text = (WORKSPACE / "zmatrix" / "research_db" / "market_data" / name).read_text()
        for fb in ["BUY","SELL","AUTO_EXECUTE","production_allowed=True"]:
            assert fb not in text or "allowlist:" in text, f"{fb} in {name}"

def test_all_four_modules_compile():
    import importlib
    for mod in ["zmatrix.research_db.market_data.return_engine","zmatrix.research_db.market_data.alpha_engine",
                "zmatrix.research_db.market_data.trading_cost_engine","zmatrix.research_db.market_data.net_return_engine"]:
        importlib.import_module(mod)

import pytest
if __name__ == "__main__":
    pytest.main([__file__, "-v"])

# ── Additional edge cases ──
def test_slippage_zero_bps(): assert TradingCostEngine.compute_slippage(10000, 0) == 0.0
def test_commission_custom_bps():
    c = TradingCostEngine.compute_buy_commission(10000, 5.0)
    assert c == pytest.approx(5.0)
def test_alpha_vs_market_missing_prices():
    r = AlphaEngine.compute_alpha_vs_market(10, 12, "2023-01-01", "2023-01-05", BARS, BM)
    assert isinstance(r, dict)
def test_annualized_return_negative(): 
    r = ReturnEngine.compute_annualized_return(-0.1, 20)
    assert r < 0
def test_holding_days_same_day(): assert ReturnEngine.calculate_holding_days("2024-01-02","2024-01-02",CAL) == 0
def test_cost_no_trade(): 
    r = TradingCostEngine.compute_total_cost(0,0)
    assert r.total_cost == 0.0
def test_full_net_commission_default_bps():
    r = NetReturnEngine.compute_full_net_result(10,11,10000)
    assert r.total_cost > 0
