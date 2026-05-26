"""Alpha RC Gate Validator tests"""
import sys, os; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from zmatrix.alpha_rc.rc_gate_validator import validate_v3_alpha_rc_gate

def test_rc_gate_passes():
    r = validate_v3_alpha_rc_gate()
    assert r["pass"] is True, f"violations: {r.get('violations', [])}"
    print("✅ RC gate passes")

def test_rc_gate_runtime_false():
    r = validate_v3_alpha_rc_gate()
    assert r["runtime_enabled"] is False
    print("✅ runtime_enabled=False")

def test_rc_gate_real_trade_false():
    r = validate_v3_alpha_rc_gate()
    assert r["real_trade_allowed"] is False
    print("✅ real_trade_allowed=False")

if __name__ == "__main__":
    test_rc_gate_passes()
    test_rc_gate_runtime_false()
    test_rc_gate_real_trade_false()
    print("\n🏁 Alpha RC Gate Validator tests PASS")
