"""Strategy Metrics tests"""
import sys,os; sys.path.insert(0,'.')
from zmatrix.brd_replay.metrics import build_strategy_metrics
from zmatrix.brd_replay.role_stats import build_role_stats

def test_metrics():
    outcomes = [
        {"actual_return_t20":0.10,"outcome_status":"READY","invalidation_triggered":False},
        {"actual_return_t20":-0.05,"outcome_status":"READY","invalidation_triggered":True}]
    r = build_strategy_metrics(outcomes=outcomes,horizon="t20")
    assert r["win_rate"] == 0.5
    assert r["invalidated_count"] == 1

def test_role_stats():
    r = build_role_stats(paper_actions=[{"paper_id":"p1","role":"A_LONG_CORE"},{"paper_id":"p2","role":"B_MID_ROTATION"}],
        outcomes=[{"paper_id":"p1","actual_return_t20":0.1,"outcome_status":"READY"},{"paper_id":"p2","actual_return_t20":-0.1,"outcome_status":"READY"}])
    assert r["role_count"] == 2

if __name__ == "__main__":
    test_metrics(); test_role_stats()
    print("\n🏁 Metrics PASS")
