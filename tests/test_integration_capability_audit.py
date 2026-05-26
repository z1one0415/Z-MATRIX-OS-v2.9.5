"""Capability Audit tests"""
import sys, os; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from zmatrix.integration.capability_audit import audit_forbidden_capabilities

def test_capability_audit_passes_for_preview_modules():
    r = audit_forbidden_capabilities()
    assert r["pass"] is True, f"violations: {r.get('violations', [])}"
    assert r["violations"] == []
    print("✅ capability audit passes")

def test_capability_audit_checks_all_registries():
    r = audit_forbidden_capabilities()
    assert set(r["checked_registries"]) == {
        "PIPELINE_REGISTRY", "WORKFLOW_DAG_REGISTRY",
        "SHARED_SKILL_REGISTRY", "GATE_REGISTRY",
    }
    print("✅ capability audit checks 4 registries")

def test_capability_audit_blocks_missing_forbidden():
    from zmatrix.architecture import pipeline_registry as pr
    original = list(pr.PIPELINE_REGISTRY["Z-TailRiskAutonomicGates"]["forbidden_capabilities"])
    pr.PIPELINE_REGISTRY["Z-TailRiskAutonomicGates"]["forbidden_capabilities"] = []
    try:
        r = audit_forbidden_capabilities()
        assert r["pass"] is False
        assert r["violations"]
    finally:
        pr.PIPELINE_REGISTRY["Z-TailRiskAutonomicGates"]["forbidden_capabilities"] = original
    print("✅ capability audit detects missing forbidden caps")

if __name__ == "__main__":
    test_capability_audit_passes_for_preview_modules()
    test_capability_audit_checks_all_registries()
    test_capability_audit_blocks_missing_forbidden()
    print("\n🏁 Capability Audit tests PASS")
