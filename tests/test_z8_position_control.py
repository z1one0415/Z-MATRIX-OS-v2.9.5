"""Z8 Position Control contract tests"""
import sys, os; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from zmatrix.investment.z8_position_control import evaluate_z8_position_control, _FORBIDDEN
import json


def test_reject_zero_position():
    r = evaluate_z8_position_control({"ticker": "002472", "role": "D_REJECT"})
    assert r["position_allowed"] is False
    assert r["max_position_size"] == 0.0
    print("✅ z8: D_REJECT → position=0")


def test_long_core_limit():
    r = evaluate_z8_position_control({"ticker": "002472", "role": "A_LONG_CORE"},
                                       {"account_gate_passed": True}, {"exposure_gate_passed": True})
    assert r["position_allowed"] is True
    assert r["max_position_size"] == 0.12
    print("✅ z8: A_LONG_CORE → max 12%")


def test_short_event_limit():
    r = evaluate_z8_position_control({"ticker": "002472", "role": "C_SHORT_EVENT"},
                                       {"account_gate_passed": True}, {"exposure_gate_passed": True})
    assert r["position_allowed"] is True
    assert r["max_position_size"] == 0.05
    print("✅ z8: C_SHORT_EVENT → max 5%")


def test_no_forbidden():
    r = evaluate_z8_position_control({"ticker": "002472", "role": "WATCH_ONLY"})
    for t in _FORBIDDEN:
        assert t not in json.dumps(r)
    print("✅ z8: no forbidden tokens")


if __name__ == "__main__":
    test_reject_zero_position(); test_long_core_limit(); test_short_event_limit(); test_no_forbidden()
    print("\n🏁 Z8 Position Control — tests PASS")
