import sys,os; sys.path.insert(0,'.')
from zmatrix.brd_strategy_validation.failure_analyzer import analyze_validation_failures

def test_failures():
    r={"daily_results":[{"rows":[{"ticker":"000001"}],"failures":[{"ticker":"000002","error":"x"}],"paper_actions":[{"paper_id":"p1","paper_action":"NO_ACTION","source_brd_result":{"fallback":False}},{"paper_id":"p2","paper_action":"DATA_GAP","source_brd_result":{"fallback":True}}],"outcomes":[{"paper_id":"p1","outcome_status":"NO_ACTION"},{"paper_id":"p2","outcome_status":"INSUFFICIENT_DATA"}]}]}
    a=analyze_validation_failures(replay_result=r)
    assert a["failure_count"]==1; assert a["fallback_count"]==1; assert a["real_trade_allowed"] is False
    print("✅ failure analyzer")

if __name__=="__main__": test_failures(); print("\n🏁 Failure Analyzer PASS")
