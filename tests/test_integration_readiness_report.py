"""Readiness Report tests"""
import sys, os; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from zmatrix.integration.readiness_report import build_v3_alpha_readiness_report

def test_readiness_report_ready_for_alpha():
    r = build_v3_alpha_readiness_report()
    assert r["overall_status"] == "READY_FOR_ALPHA", f"status={r['overall_status']}"
    assert r["ready_for_alpha"] is True
    assert r["alpha_runtime_allowed"] is False
    assert r["real_trade_allowed"] is False
    assert r["blocking_issues"] == []
    print("✅ READY_FOR_ALPHA, runtime=False, trade=False, blocking=[]")

def test_readiness_report_real_trade_false():
    r = build_v3_alpha_readiness_report()
    assert r["readiness_semantics"]["runtime_allowed"] is False
    assert r["readiness_semantics"]["real_trade_allowed"] is False
    print("✅ readiness semantics: runtime/trade False")

def test_readiness_report_all_sections_pass():
    r = build_v3_alpha_readiness_report()
    for section in ["capability_audit", "workflow_alignment", "event_chain_validation", "safety_matrix"]:
        assert r[section]["pass"] is True, f"{section} not passing"
    print("✅ all readiness sections pass")

if __name__ == "__main__":
    test_readiness_report_ready_for_alpha()
    test_readiness_report_real_trade_false()
    test_readiness_report_all_sections_pass()
    print("\n🏁 Readiness Report tests PASS")
