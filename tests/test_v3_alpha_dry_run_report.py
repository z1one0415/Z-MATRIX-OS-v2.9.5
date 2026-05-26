"""Dry-Run Report tests"""
import sys, os; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from zmatrix.dry_run.rehearsal_report import build_v3_alpha_dry_run_report

def test_dry_run_report_passes():
    r = build_v3_alpha_dry_run_report()
    assert r["overall_status"] == "PASS"
    assert r["dry_run_pass"] is True
    assert r["blocking_issues"] == []
    print("✅ dry-run report passes")

def test_dry_run_report_runtime_false():
    r = build_v3_alpha_dry_run_report()
    assert r["runtime_enabled"] is False
    print("✅ runtime_enabled=False")

def test_dry_run_report_real_trade_false():
    r = build_v3_alpha_dry_run_report()
    assert r["real_trade_allowed"] is False
    print("✅ real_trade_allowed=False")

if __name__ == "__main__":
    test_dry_run_report_passes()
    test_dry_run_report_runtime_false()
    test_dry_run_report_real_trade_false()
    print("\n🏁 Dry-Run Report tests PASS")
