"""Summary Report tests"""
import sys,os; sys.path.insert(0,'.')
from zmatrix.paper_outcome.summary_report import build_outcome_summary

def test_summary():
    results = [{"outcome_status":"READY","actual_return_t5":3.0,"actual_return_t20":5.0},
               {"outcome_status":"READY","actual_return_t5":-1.0,"actual_return_t20":-2.0},
               {"outcome_status":"INSUFFICIENT_DATA"}]
    r = build_outcome_summary(results)
    assert r["total_ready"] == 2
    assert r["win_rate_t20"] is not None
    print(f"✅ summary: win_rate={r['win_rate_t20']}%")

if __name__ == "__main__":
    test_summary()
    print("\n🏁 Summary Report PASS")
