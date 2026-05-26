import sys,os; sys.path.insert(0,'.')
from zmatrix.brd_result_audit.active_outcome_validator import validate_active_outcomes

def test_pass():
    r=validate_active_outcomes(paper_actions=[{"paper_id":"p1","ticker":"000001","paper_action":"PAPER_WATCH_ROTATION"},{"paper_id":"p2","ticker":"000002","paper_action":"NO_ACTION"}],outcomes=[{"paper_id":"p1","outcome_status":"READY","actual_return_t20":0.1},{"paper_id":"p2","outcome_status":"NO_ACTION"}])
    assert r["active_paper_actions"]==1; assert r["status"]=="PASS"; assert r["real_trade_allowed"] is False
    print(f"✅ outcome: active={r['active_paper_actions']} ready={r['ready_outcomes']}")

def test_blocks():
    r=validate_active_outcomes(paper_actions=[],outcomes=[]); assert r["status"]=="BLOCKED_NO_ACTIVE_ACTIONS"
    print("✅ blocks no active")

if __name__=="__main__": test_pass(); test_blocks(); print("\n🏁 Outcome Validator PASS")
