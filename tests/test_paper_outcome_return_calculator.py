"""Return Calculator tests"""
import sys,os; sys.path.insert(0,'.')
from zmatrix.paper_outcome.return_calculator import calc_all_horizons

def test_calc_all_horizons():
    r = calc_all_horizons(50.0, [51,52,53,54,55,56]*20)
    assert r["actual_return_t5"] is not None
    assert r["actual_return_t20"] is not None
    assert r["actual_return_t60"] is not None
    print("✅ calc_all_horizons works")

def test_no_data_returns_none():
    r = calc_all_horizons(0, [])
    assert r["actual_return_t5"] is None
    print("✅ no data returns None")

if __name__ == "__main__":
    test_calc_all_horizons()
    test_no_data_returns_none()
    print("\n🏁 Return Calculator PASS")
