"""Replay Universe tests — PIT cutoff"""
import sys,os; sys.path.insert(0,'.')
from zmatrix.historical_replay.replay_universe import build_replay_universe

def test_replay_universe_no_future_data():
    r = build_replay_universe(replay_date="2024-06-03", local_data_root=".")
    assert r["future_data_allowed"] is False
    print("✅ no future data")

def test_replay_universe_has_filters():
    r = build_replay_universe(replay_date="2024-06-03", local_data_root=".")
    assert r["filters"]["point_in_time_only"] is True
    print("✅ PIT filter active")

if __name__ == "__main__":
    test_replay_universe_no_future_data()
    test_replay_universe_has_filters()
    print("\n🏁 Replay Universe PASS")
