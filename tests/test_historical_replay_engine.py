"""Replay Engine tests — real data"""
import sys,os; sys.path.insert(0,'.')
from zmatrix.historical_replay.replay_engine import run_single_day_replay

def test_replay_engine_no_real_trade():
    r = run_single_day_replay(replay_date="2024-06-03", local_data_root=".", max_tickers=5)
    assert r["real_trade_allowed"] is False
    assert "tickers_with_data" in r
    assert "tickers_without_data" in r
    print(f"✅ engine: {r['tickers_with_data']}/{r['tickers_scanned']} with data")

if __name__ == "__main__":
    test_replay_engine_no_real_trade()
    print("\n🏁 Replay Engine PASS")
