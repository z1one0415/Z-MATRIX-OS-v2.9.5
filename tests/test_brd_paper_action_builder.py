"""Paper Action Builder tests"""
import sys,os; sys.path.insert(0,'.')
from zmatrix.brd_replay.paper_action_builder import build_paper_action_from_brd

def test_a_long_core():
    r = build_paper_action_from_brd(replay_date="2024-06-03",ticker="000001",
        brd_result={"role":"A_LONG_CORE","hard_gate_passed":True,"brd_score":80},price_snapshot={"close":10})
    assert r["paper_action"] == "PAPER_WATCH_CORE"
    assert r["real_trade_allowed"] is False

def test_d_reject_no_action():
    r = build_paper_action_from_brd(replay_date="2024-06-03",ticker="000001",
        brd_result={"role":"D_REJECT","hard_gate_passed":True},price_snapshot={"close":10})
    assert r["paper_action"] == "NO_ACTION"

if __name__ == "__main__":
    test_a_long_core(); test_d_reject_no_action()
    print("\n🏁 Paper Action PASS")
