"""BRD Input Bundle tests"""
import sys,os,tempfile,csv; sys.path.insert(0,'.')
from pathlib import Path
from zmatrix.brd_matrix_pit.brd_input_bundle_builder import build_brd_input_bundle

def _write_fund(path):
    path.parent.mkdir(parents=True,exist_ok=True)
    with open(path,"w",newline="",encoding="utf-8") as f:
        csv.writer(f).writerows([["ticker","ann_date","roe","gross_margin","revenue_yoy","profit_yoy","debt_ratio","pe","pb"],["000001","20240501","12","30","10","12","40","15","1.5"]])

def test_bundle():
    with tempfile.TemporaryDirectory() as d:
        root = Path(d)
        _write_fund(root/"data"/"fundamentals"/"000001.csv")
        bundle = build_brd_input_bundle(ticker="000001",replay_date="20240603",local_data_root=str(root),
            pit_features={"feature_status":"READY","history_days":150,"features":{"return_5d":0.02,"return_20d":0.08,"return_60d":0.15,"above_ma20":True,"above_ma60":True,"above_ma120":True,"volume_ratio_20d":1.2,"volatility_20d":0.03,"volatility_60d":0.04}})
        assert bundle["input_ready"] is True
        assert bundle["real_trade_allowed"] is False
        print(f"✅ bundle: b_status={bundle['b_matrix']['status']} r={bundle['r_matrix']['status']} d={bundle['d_matrix']['status']}")

if __name__ == "__main__":
    test_bundle()
    print("\n🏁 Input Bundle PASS")
