"""Readiness Report tests"""
import sys, os; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from zmatrix.integration.readiness_report import build_v3_alpha_readiness_report

def test_readiness_report_ready_for_alpha_but_runtime_false():
    r = build_v3_alpha_readiness_report()
    assert r["alpha_runtime_allowed"] is False
    print(f"✅ overall_status={r['overall_status']} runtime=False")

def test_readiness_report_real_trade_false():
    r = build_v3_alpha_readiness_report()
    assert r["real_trade_allowed"] is False
    print("✅ real_trade_allowed=False")

def test_readiness_report_has_all_sections():
    r = build_v3_alpha_readiness_report()
    for section in ["capability_audit", "workflow_alignment", "event_chain_validation", "safety_matrix"]:
        assert section in r
    print(f"✅ readiness report has {len(r)} top-level keys")

if __name__ == "__main__":
    test_readiness_report_ready_for_alpha_but_runtime_false()
    test_readiness_report_real_trade_false()
    test_readiness_report_has_all_sections()
    print("\n🏁 Readiness Report tests PASS")
