#!/usr/bin/env python3
"""System Controller MVP v1.0 — Batch F-8 tests"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from zmatrix.architecture.system_controller import build_system_execution_plan


def test_build_plan_for_g18_workflow():
    plan = build_system_execution_plan("Z-G18.paper_z9_preview_workflow")
    assert plan["controller_version"] == "v1.0"
    assert plan["workflow_id"] == "Z-G18.paper_z9_preview_workflow"
    assert plan["pipeline_id"] == "Z-G18"
    print("✅ plan: Z-G18 workflow loaded")


def test_execution_allowed_false():
    plan = build_system_execution_plan("Z-G18.paper_z9_preview_workflow")
    assert plan["execution_allowed"] is False
    print("✅ plan: execution_allowed=False")


def test_real_ops_allowed_false():
    plan = build_system_execution_plan("Z-G18.paper_z9_preview_workflow")
    assert plan["real_ops_allowed"] is False
    print("✅ plan: real_ops_allowed=False")


def test_ordered_nodes_contains_full_z9_chain():
    plan = build_system_execution_plan("Z-G18.paper_z9_preview_workflow")
    nodes = plan["ordered_nodes"]
    assert "z9.sample.build" in nodes
    assert "z9.queue.build" in nodes
    assert "z9.backfill_task.build" in nodes
    assert "z9.calibration_policy.preview" in nodes
    assert nodes[-1] == "z9.calibration_policy.preview"
    assert nodes[0] == "r_matrix.evaluate_cycle"
    print(f"✅ plan: ordered_nodes ({len(nodes)} nodes) with full Z9 chain")


def test_missing_workflow_rejected():
    plan = build_system_execution_plan("nonexistent")
    assert plan["reason"] == "WORKFLOW_NOT_FOUND"
    assert plan["execution_allowed"] is False
    print("✅ plan: missing workflow rejected")


def test_no_runtime_execution():
    plan = build_system_execution_plan("Z-G18.paper_z9_preview_workflow")
    assert "empty G18" not in str(plan)  # 不实际调用
    assert plan["validation"]["ready_for_runtime"] is False
    assert plan["reason"] == "SYSTEM_CONTROLLER_MVP_PLAN_ONLY_NO_RUNTIME_EXECUTION"
    print("✅ plan: no runtime execution, plan only")


def test_all_gates_registered():
    plan = build_system_execution_plan("Z-G18.paper_z9_preview_workflow")
    assert plan["validation"]["gates_registered"] is True
    expected_gates = {"safety.no_real_trade", "contract.validation", "z9.preview_only"}
    actual_gates = set(plan["required_gates"])
    assert expected_gates == actual_gates
    print("✅ plan: all required gates registered")


def test_rc_workflow_plan():
    plan = build_system_execution_plan("RC.release_verification_workflow")
    assert plan["pipeline_id"] == "RC-release"
    assert "rc.checksum.build" in plan["ordered_nodes"]
    assert plan["execution_allowed"] is False
    print("✅ plan: RC workflow plan (checksum/packaging/verification/safety)")


def test_dry_run_default():
    plan = build_system_execution_plan("Z-G18.paper_z9_preview_workflow")
    assert plan["dry_run"] is True
    print("✅ plan: dry_run=True by default")


def test_forbidden_capabilities_propagated():
    plan = build_system_execution_plan("Z-G18.paper_z9_preview_workflow")
    fc = plan["forbidden_capabilities"]
    for r in ["real_trade", "real_z9_write", "real_market_fetch", "auto_calibration"]:
        assert r in fc, f"missing: {r}"
    print("✅ plan: forbidden_capabilities propagated")


if __name__ == "__main__":
    test_build_plan_for_g18_workflow()
    test_execution_allowed_false()
    test_real_ops_allowed_false()
    test_ordered_nodes_contains_full_z9_chain()
    test_missing_workflow_rejected()
    test_no_runtime_execution()
    test_all_gates_registered()
    test_rc_workflow_plan()
    test_dry_run_default()
    test_forbidden_capabilities_propagated()
    print("\n🏁 System Controller MVP v1.0 — all F-8 tests PASS")
