"""Matrix PIT Policy tests"""
import sys,os; sys.path.insert(0,'.')
from zmatrix.brd_matrix_pit.pit_brd_matrix_policy import assert_no_matrix_runtime_effects

def test_rejects_real_trade():
    assert any("real_trade_allowed" in e for e in assert_no_matrix_runtime_effects({"real_trade_allowed":True}))

def test_rejects_safety_runtime():
    assert any("safety.runtime_enabled" in e for e in assert_no_matrix_runtime_effects({"safety":{"runtime_enabled":True}}))

if __name__ == "__main__":
    test_rejects_real_trade(); test_rejects_safety_runtime()
    print("\n🏁 Matrix Policy PASS")
