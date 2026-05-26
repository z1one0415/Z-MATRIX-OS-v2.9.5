"""Real BRD Connector tests"""
import sys,os; sys.path.insert(0,'.')
from zmatrix.brd_replay.real_brd_connector import build_real_brd_classifier_connector

def test_connector_builds():
    c = build_real_brd_classifier_connector()
    assert c.connector_status in ("CONNECTED","NOT_FOUND","ERROR")
    assert hasattr(c,"classify")
    print(f"✅ status={c.connector_status}")

def test_connector_no_trade():
    c = build_real_brd_classifier_connector()
    r = c.classify({"feature_status":"READY","features":{}})
    assert r["real_trade_allowed"] is False
    assert r["broker_order_allowed"] is False
    print("✅ no trade")

if __name__ == "__main__":
    test_connector_builds(); test_connector_no_trade()
    print("\n🏁 Real Connector PASS")
