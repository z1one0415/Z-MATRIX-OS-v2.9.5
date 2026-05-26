"""Connection Validator tests"""
import sys,os; sys.path.insert(0,'.')
from zmatrix.brd_replay.connection_validator import validate_brd_connection_report

def test_passes_connected_low_fallback():
    r = validate_brd_connection_report({"brd_connected":True,"fallback_rate":0.01})
    assert r["pass"] is True

def test_blocks_not_connected():
    r = validate_brd_connection_report({"brd_connected":False,"fallback_rate":1.0})
    assert r["pass"] is False

def test_blocks_high_fallback():
    r = validate_brd_connection_report({"brd_connected":True,"fallback_rate":0.20})
    assert r["pass"] is False

if __name__ == "__main__":
    test_passes_connected_low_fallback(); test_blocks_not_connected(); test_blocks_high_fallback()
    print("\n🏁 Connection Validator PASS")
