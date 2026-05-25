"""Monthly Review tests"""
import sys, os; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from zmatrix.paper_trading.monthly_review import build_monthly_review

def test_review_fields():
    r = build_monthly_review(
        [{"paper_id":"1","ticker":"002472","role":"A_LONG_CORE"},{"paper_id":"2","ticker":"601899","role":"B_MID_ROTATION"}],
        [{"paper_id":"1","actual_return_t20":5},{"paper_id":"2","actual_return_t20":-3}])
    assert r["paper_count"] == 2
    assert r["win_rate"] == 50.0
    assert r["real_trade_allowed"] is False
    assert r["role_breakdown"].get("A_LONG_CORE") == 1
    print(f"✅ monthly review: {r['paper_count']} papers, win_rate={r['win_rate']}%")

def test_empty():
    r = build_monthly_review([], [])
    assert r["paper_count"] == 0
    print("✅ monthly review: empty")

if __name__ == "__main__":
    test_review_fields(); test_empty()
    print("\n🏁 Monthly Review — tests PASS")
