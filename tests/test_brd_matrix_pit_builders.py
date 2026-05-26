"""PIT Matrix Builders tests"""
import sys,os; sys.path.insert(0,'.')
from zmatrix.brd_matrix_pit.r_matrix_pit_builder import build_r_matrix_pit
from zmatrix.brd_matrix_pit.d_matrix_pit_builder import build_d_matrix_pit
from zmatrix.brd_matrix_pit.b_matrix_pit_builder import build_b_matrix_pit

def test_r_matrix():
    r = build_r_matrix_pit(ticker="000001",replay_date="20240603",pit_features={"feature_status":"READY",
        "features":{"return_5d":0.02,"return_20d":0.08,"return_60d":0.15,"above_ma20":True,"above_ma60":True,"above_ma120":True,"volume_ratio_20d":1.2,"volatility_20d":0.03,"volatility_60d":0.04}})
    assert r["status"] in ("PASS","FAIL"); assert r["real_trade_allowed"] is False
    print(f"✅ R-Matrix: status={r['status']} phase={r['sector_phase']}")

def test_d_no_event():
    d = build_d_matrix_pit(ticker="000001",replay_date="20240603",pit_features={"feature_status":"READY",
        "features":{"return_5d":0.10,"return_20d":0.20,"volume_ratio_20d":2.0,"volatility_20d":0.03}})
    assert d["status"] == "FAIL"; assert d["event_data_missing"] is True
    print("✅ D-Matrix: no event → FAIL")

def test_b_no_fund():
    b = build_b_matrix_pit(ticker="000001",replay_date="20240603",local_data_root="/tmp/nonexistent")
    assert b["status"] == "FAIL"
    print("✅ B-Matrix: no fund → FAIL")

if __name__ == "__main__":
    test_r_matrix(); test_d_no_event(); test_b_no_fund()
    print("\n🏁 Matrix PIT Builders PASS")
