"""BRD Classifier Connection tests"""
import sys,os; sys.path.insert(0,'.')
from zmatrix.brd_replay.brd_classifier_adapter import run_brd_classifier_adapter

def mock_c(features):
    return {"role":"B_MID_ROTATION","decision":"BUY","role_confidence":0.77,"brd_score":83,"hard_gate_passed":True,"brd_connected":True}

def test_mock_connects():
    r = run_brd_classifier_adapter(ticker="000001",replay_date="2024-06-03",
        pit_features={"feature_status":"READY","features":{"close":10}},classifier=mock_c)
    assert r["brd_connected"] is True
    assert r["fallback"] is False
    assert r["decision"] == "WATCH_ONLY"
    assert r["real_trade_allowed"] is False

def test_no_classifier_no_fake():
    r = run_brd_classifier_adapter(ticker="000001",replay_date="2024-06-03",
        pit_features={"feature_status":"READY","features":{"close":10}},classifier=None)
    if r["brd_connected"] is False:
        assert r["fallback"] is True

if __name__ == "__main__":
    test_mock_connects(); test_no_classifier_no_fake()
    print("\n🏁 Classifier Connection PASS")
