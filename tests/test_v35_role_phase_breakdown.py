import sys,os; sys.path.insert(0,'.')
from zmatrix.brd_strategy_validation.role_breakdown import build_role_breakdown
from zmatrix.brd_strategy_validation.phase_breakdown import build_phase_breakdown

def test_breakdown():
    r={"daily_results":[{"paper_actions":[{"paper_id":"p1","role":"B_MID_ROTATION","sector_phase":"主升","paper_action":"PAPER_WATCH_ROTATION"},{"paper_id":"p2","role":"D_REJECT","sector_phase":"退潮","paper_action":"NO_ACTION"}],"outcomes":[{"paper_id":"p1","outcome_status":"READY","actual_return_t20":0.08},{"paper_id":"p2","outcome_status":"NO_ACTION"}]}]}
    roles=build_role_breakdown(replay_result=r,horizon="t20")
    phases=build_phase_breakdown(replay_result=r,horizon="t20")
    assert "B_MID_ROTATION" in roles["roles"]; assert "D_REJECT" not in roles["roles"]
    assert "主升" in phases["phases"]; assert phases["real_trade_allowed"] is False
    print("✅ role+phase breakdown")

if __name__=="__main__": test_breakdown(); print("\n🏁 Role/Phase PASS")
