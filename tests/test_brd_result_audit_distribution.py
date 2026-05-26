import sys,os; sys.path.insert(0,'.')
from zmatrix.brd_result_audit.market_role_distribution import build_market_role_distribution_report

def test_distribution():
    actions=[{"paper_id":"p1","role":"A_LONG_CORE","paper_action":"PAPER_WATCH_CORE"},{"paper_id":"p2","role":"B_MID_ROTATION","paper_action":"PAPER_WATCH_ROTATION"},{"paper_id":"p3","role":"D_REJECT","paper_action":"NO_ACTION"}]*400
    r=build_market_role_distribution_report(paper_actions=actions)
    assert r["total"]==1200; assert r["role_distribution"]["A_LONG_CORE"]["count"]==400
    assert r["active_paper_actions"]==800; assert r["real_trade_allowed"] is False
    print(f"✅ distribute: A={r['role_distribution']['A_LONG_CORE']['rate']} B={r['role_distribution']['B_MID_ROTATION']['rate']}")

if __name__=="__main__": test_distribution(); print("\n🏁 Distribution PASS")
