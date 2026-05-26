"""Dry-Run Validator tests"""
import sys, os; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from zmatrix.dry_run.rehearsal_runner import build_v3_alpha_dry_run_rehearsal
from zmatrix.dry_run.rehearsal_validator import validate_v3_alpha_dry_run_rehearsal

def test_dry_run_validation_passes():
    r = build_v3_alpha_dry_run_rehearsal()
    v = validate_v3_alpha_dry_run_rehearsal(r)
    assert v["pass"] is True, f"violations: {v.get('violations', [])}"
    print("✅ dry-run validation passes")

def test_validator_rejects_runtime_enabled_true():
    r = build_v3_alpha_dry_run_rehearsal()
    r["runtime_enabled"] = True
    v = validate_v3_alpha_dry_run_rehearsal(r)
    assert v["pass"] is False
    print("✅ rejects runtime_enabled=True")

def test_validator_rejects_real_trade_true():
    r = build_v3_alpha_dry_run_rehearsal()
    r["real_trade_allowed"] = True
    v = validate_v3_alpha_dry_run_rehearsal(r)
    assert v["pass"] is False
    print("✅ rejects real_trade_allowed=True")

if __name__ == "__main__":
    test_dry_run_validation_passes()
    test_validator_rejects_runtime_enabled_true()
    test_validator_rejects_real_trade_true()
    print("\n🏁 Dry-Run Validator tests PASS")
