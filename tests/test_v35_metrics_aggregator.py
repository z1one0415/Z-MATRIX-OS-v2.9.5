import sys,os; sys.path.insert(0,'.')
from zmatrix.brd_strategy_validation.metrics_aggregator import aggregate_validation_metrics

def test_metrics():
    r = aggregate_validation_metrics(replay_result={"daily_results":[{"paper_actions":[{"paper_id":"p1","paper_action":"PAPER_WATCH_ROTATION"},{"paper_id":"p2","paper_action":"NO_ACTION"}],"outcomes":[{"paper_id":"p1","outcome_status":"READY","actual_return_t20":0.1},{"paper_id":"p2","outcome_status":"NO_ACTION"}]}]},horizon="t20")
    assert r["active_paper_actions"]==1; assert r["t20"]["win_rate"]==1.0; assert r["real_trade_allowed"] is False
    print("✅ metrics aggregator")

if __name__=="__main__": test_metrics(); print("\n🏁 Metrics PASS")
