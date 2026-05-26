"""BRD Classifier Adapter tests"""
import sys,os; sys.path.insert(0,'.')
from zmatrix.brd_replay.brd_classifier_adapter import run_brd_classifier_adapter

def test_fallback_when_no_classifier():
    r = run_brd_classifier_adapter(ticker="000001",replay_date="2024-06-03",
        pit_features={"feature_status":"READY","features":{}})
    assert r["fallback"] is True
    assert r["brd_connected"] is False
    print("✅ fallback=BRD_NOT_CONNECTED")

def test_no_BUY_decision():
    r = run_brd_classifier_adapter(ticker="000001",replay_date="2024-06-03",
        pit_features={"feature_status":"READY","features":{}},
        classifier=lambda f: {"role":"A_LONG_CORE","decision":"BUY","brd_score":80,"hard_gate_passed":True})
    assert r["decision"] == "WATCH_ONLY"
    print("✅ BUY downgraded to WATCH_ONLY")

if __name__ == "__main__":
    test_fallback_when_no_classifier(); test_no_BUY_decision()
    print("\n🏁 BRD Classifier PASS")
