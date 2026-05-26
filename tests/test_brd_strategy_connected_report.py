"""Strategy Connected Report tests — mock classifier with synthetic bundle"""
import sys,os,tempfile,csv; sys.path.insert(0,'.')
from pathlib import Path
from zmatrix.brd_replay.multi_day_runner import run_multi_day_brd_strategy_replay
from zmatrix.brd_replay.strategy_validation_report import build_brd_strategy_validation_report

def _write_stock(path):
    path.parent.mkdir(parents=True,exist_ok=True)
    with open(path,"w",newline="",encoding="utf-8") as f:
        cw=csv.writer(f); cw.writerow(["trade_date","open","high","low","close","volume"])
        # 200 trading days before 20240415 = start from 20230801
        import datetime
        d = datetime.date(2023, 8, 1)
        for i in range(200):
            cw.writerow([d.strftime("%Y%m%d"), "10","11","9",str(10+i*0.01),"10000"])
            d += datetime.timedelta(days=1)

def mock_c(pit_features):
    bundle = pit_features.get("brd_input_bundle",{})
    b = bundle.get("b_matrix",{})
    return {"role":"B_MID_ROTATION" if b.get("status")=="PASS" else "B_MID_ROTATION",
            "role_confidence":0.8,"brd_score":85,"hard_gate_passed":True,"brd_connected":True}

def test_connected_report():
    with tempfile.TemporaryDirectory() as d:
        root = Path(d)
        _write_stock(root/"data"/"price_bars"/"000001.csv")
        replay = run_multi_day_brd_strategy_replay(replay_dates=["20240415"],local_data_root=str(root),max_tickers=1,classifier=mock_c)
        report = build_brd_strategy_validation_report(replay_result=replay,horizon="t20")
        assert report["brd_connected"] is True, f"expected brd_connected=True, got {report['brd_connected']}"
        assert report["validation_status"] == "BRD_CONNECTED_STRATEGY_VALIDATION_READY", f"got {report['validation_status']}"
        print(f"✅ connected: brd={report['brd_connected']} status={report['validation_status']}")

if __name__ == "__main__":
    test_connected_report()
    print("\n🏁 Connected Report PASS")
