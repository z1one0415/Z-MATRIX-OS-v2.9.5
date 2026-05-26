"""Approval Policy tests"""
import sys, os; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from zmatrix.approval_loop.approval_policy import assert_no_auto_effects, validate_approval_request

def test_policy_rejects_auto_effects_true():
    record = {"safety": {"real_trade_allowed": True, "auto_calibration_allowed": True}}
    v = assert_no_auto_effects(record)
    assert len(v) >= 2
    print("✅ policy rejects auto effects")

def test_policy_passes_clean_record():
    record = {"safety": {"real_trade_allowed": False, "auto_calibration_allowed": False}}
    v = assert_no_auto_effects(record)
    assert len(v) == 0
    print("✅ policy passes clean record")

if __name__ == "__main__":
    test_policy_rejects_auto_effects_true()
    test_policy_passes_clean_record()
    print("\n🏁 Approval Policy tests PASS")
