"""Chain Force 10×5 contract tests"""
import sys, os; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from zmatrix.investment.chain_force import evaluate_chain_force_10x5, _FORBIDDEN
import json


def test_degraded_on_missing_data():
    r = evaluate_chain_force_10x5({"ticker": "002472"})
    assert r["degraded"] is True
    assert r["chain_status"] == "UNKNOWN"
    print("✅ chain_force: DEGRADED on missing data")


def test_favorable():
    r = evaluate_chain_force_10x5({"ticker": "002472", "force_scores": {"fin": 8, "geo": 7, "state": 9}})
    assert r["chain_gate_passed"] is True
    assert r["chain_status"] == "FAVORABLE"
    print("✅ chain_force: FAVORABLE")


def test_no_forbidden():
    r = evaluate_chain_force_10x5({"ticker": "002472"})
    for t in _FORBIDDEN:
        assert t not in json.dumps(r)
    print("✅ chain_force: no forbidden tokens")


if __name__ == "__main__":
    test_degraded_on_missing_data(); test_favorable(); test_no_forbidden()
    print("\n🏁 Chain Force 10×5 — tests PASS")
