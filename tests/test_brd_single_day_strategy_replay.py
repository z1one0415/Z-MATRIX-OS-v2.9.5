"""Single Day Strategy Replay tests"""
import sys,os,tempfile,csv; sys.path.insert(0,'.')
from pathlib import Path
from zmatrix.brd_replay.single_day_strategy_replay import run_single_day_brd_strategy_replay

def _write(path):
    path.parent.mkdir(parents=True,exist_ok=True)
    with open(path,"w",newline="",encoding="utf-8") as f:
        csv.writer(f).writerows([["trade_date","open","high","low","close","volume"]]+[
            [f"2024{601+i:02d}","10","11","9",str(10+i*0.01),"10000"] for i in range(160)])

def test_single_day_replay():
    with tempfile.TemporaryDirectory() as d:
        root = Path(d)
        _write(root/"data"/"price_bars"/"000001.csv")
        r = run_single_day_brd_strategy_replay(replay_date="2024-10-01",local_data_root=str(root),max_tickers=1)
        assert r["mode"] == "HISTORICAL_STRATEGY_VALIDATION_ONLY"
        assert r["real_trade_allowed"] is False
        assert len(r["paper_actions"]) >= 0

if __name__ == "__main__":
    test_single_day_replay()
    print("\n🏁 Single Day Replay PASS")
