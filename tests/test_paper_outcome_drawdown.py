"""Drawdown Calculator tests"""
import sys,os; sys.path.insert(0,'.')
from zmatrix.paper_outcome.drawdown_calculator import calc_max_drawdown, calc_all_drawdowns

def test_calc_max_drawdown():
    dd = calc_max_drawdown([50,55,60,45,50,65])
    assert dd is not None and dd > 0
    print(f"✅ max_dd={dd}%")

def test_calc_all_drawdowns():
    path = list(range(50, 120, 1))
    r = calc_all_drawdowns(path)
    assert r["max_drawdown_t20"] is not None
    assert r["max_drawdown_t60"] is not None
    print("✅ calc_all_drawdowns works")

if __name__ == "__main__":
    test_calc_max_drawdown()
    test_calc_all_drawdowns()
    print("\n🏁 Drawdown PASS")
