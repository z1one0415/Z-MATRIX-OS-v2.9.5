"""Strategy Validation Report tests"""
import sys,os; sys.path.insert(0,'.')
from zmatrix.brd_replay.strategy_validation_report import build_brd_strategy_validation_report

def test_report():
    r = build_brd_strategy_validation_report(replay_result={
        "date_count":1,"success_day_count":1,"failure_day_count":0,
        "daily_results":[{"paper_actions":[{"paper_id":"p1","role":"A_LONG_CORE","source_brd_result":{"fallback_reason":""}}],
            "outcomes":[{"paper_id":"p1","actual_return_t20":0.1,"outcome_status":"READY"}]}]})
    assert r["total_paper_actions"] == 1
    assert r["brd_connected"] is True
    assert r["real_trade_allowed"] is False

if __name__ == "__main__":
    test_report()
    print("\n🏁 Report PASS")
