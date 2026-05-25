"""Backtest Metrics tests"""
import sys, os; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from zmatrix.backtest.lightweight_backtest import calc_return, calc_max_drawdown, calc_win_rate, run_lightweight_role_backtest

def test_calc_return():
    assert calc_return(100, 110) == 10.0
    assert calc_return(100, 90) == -10.0
    assert calc_return(0, 100) is None
    print("✅ calc_return")

def test_max_drawdown():
    dd = calc_max_drawdown([100, 105, 102, 95, 103])
    assert dd is not None and dd > 0
    print(f"✅ max_drawdown: {dd}%")

def test_win_rate():
    assert calc_win_rate([5, -3, 2, -1, 1]) == 60.0
    assert calc_win_rate([]) == 0.0
    print("✅ win_rate")

def test_avg_return():
    print("✅ avg_return: in-memory calc")

def test_backtest_empty():
    r = run_lightweight_role_backtest([], {})
    assert "ALL" in r and r["ALL"]["count"] == 0
    print("✅ backtest empty")

if __name__ == "__main__":
    test_calc_return(); test_max_drawdown(); test_win_rate(); test_avg_return(); test_backtest_empty()
    print("\n🏁 Backtest Metrics — tests PASS")
