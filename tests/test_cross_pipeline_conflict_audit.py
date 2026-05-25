#!/usr/bin/env python3
"""Cross-Pipeline Conflict Audit v1.0 — Batch F-6 tests"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from zmatrix.architecture.conflict_audit import (
    audit_shared_skill_usage,
    audit_pipeline_skill_conflicts,
    audit_gate_coverage_gaps,
    audit_rmatrix_single_source_of_truth,
    audit_z9_preview_boundary_consistency,
    run_cross_pipeline_conflict_audit,
)


def test_audit_result_clean():
    v = run_cross_pipeline_conflict_audit()
    assert len(v) == 0, f"audit violations: {v}"
    print("✅ cross-pipeline conflict audit: clean")


def test_rmatrix_single_source_of_truth():
    v = audit_rmatrix_single_source_of_truth()
    assert len(v) == 0, f"R-Matrix violations: {v}"
    print("✅ audit: R-Matrix single source of truth")


def test_z9_preview_chain_complete():
    v = audit_z9_preview_boundary_consistency()
    assert len(v) == 0, f"Z9 boundary violations: {v}"
    print("✅ audit: Z9 preview chain complete")


def test_no_missing_safety_gate():
    v = audit_gate_coverage_gaps()
    # 允许 applies_to 比 required_gates 宽泛，pipeline 可以不显式列出全局 gate
    # 只检查 critical gap: Z-G18 没有 z9.preview_only
    critical = [g for g in v if "z9.preview_only" in g and "Z-G18" in g]
    assert len(critical) == 0, f"critical gate coverage gaps: {critical}"
    print(f"✅ audit: no critical gate coverage gaps (non-blocking: {len(v)} non-critical)")


def test_no_pipeline_skill_conflicts():
    v = audit_pipeline_skill_conflicts()
    assert len(v) == 0, f"skill conflicts: {v}"
    print("✅ audit: no pipeline skill conflicts")


def test_shared_skill_usage_api():
    usage = audit_shared_skill_usage()
    assert "Z-G18" in usage
    assert len(usage["Z-G18"]) >= 8
    print(f"✅ audit: shared skill usage API works (Z-G18: {len(usage['Z-G18'])} skills)")


if __name__ == "__main__":
    test_audit_result_clean()
    test_rmatrix_single_source_of_truth()
    test_z9_preview_chain_complete()
    test_no_missing_safety_gate()
    test_no_pipeline_skill_conflicts()
    test_shared_skill_usage_api()
    print("\n🏁 Cross-Pipeline Conflict Audit v1.0 — all F-6 tests PASS")
