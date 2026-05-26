"""PIT Feature Builder tests"""
import sys,os,tempfile,csv; sys.path.insert(0,'.')
from pathlib import Path
from zmatrix.brd_replay.pit_feature_builder import build_pit_features

def _write_bars(path, count=130):
    path.parent.mkdir(parents=True,exist_ok=True)
    rows = [["trade_date","open","high","low","close","vol","amount"]]
    for i in range(count):
        rows.append([f"2024{str(601+i).zfill(4)}","10","11","9",str(10+i*0.01),"10000","100000"])
    with open(path,"w",newline="",encoding="utf-8") as f: csv.writer(f).writerows(rows)

def test_pit_features_ready():
    with tempfile.TemporaryDirectory() as d:
        root = Path(d)
        _write_bars(root/"data"/"price_bars"/"000001.csv")
        r = build_pit_features(ticker="000001",replay_date="2024-10-01",local_data_root=str(root),min_history_days=30)
        assert r["feature_status"] == "READY"
        assert r["features"]["close"] > 0
        print(f"✅ PIT: close={r['features']['close']:.2f}")

def test_pit_no_future_leak():
    with tempfile.TemporaryDirectory() as d:
        root = Path(d)
        _write_bars(root/"data"/"price_bars"/"000001.csv")
        r = build_pit_features(ticker="000001",replay_date="2024-06-01",local_data_root=str(root))
        assert r["future_data_allowed"] is False
        print("✅ no future leak")

if __name__ == "__main__":
    test_pit_features_ready(); test_pit_no_future_leak()
    print("\n🏁 PIT Features PASS")
