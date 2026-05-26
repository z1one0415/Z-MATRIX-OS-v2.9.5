"""Replay Universe tests"""
import sys,os; sys.path.insert(0,'.')
from zmatrix.historical_replay.replay_universe import build_replay_universe

def test_replay_universe_no_future_data():
    r = build_replay_universe(replay_date="2024-06-03", local_data_root=".")
    assert r["future_data_allowed"] is False
    print("✅ no future data")

if __name__ == "__main__":
    test_replay_universe_no_future_data()
    print("\n🏁 Replay Universe PASS")
