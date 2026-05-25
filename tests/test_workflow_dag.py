#!/usr/bin/env python3
"""Workflow DAG Registry v1.0 — Batch F-4 contract tests"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from zmatrix.architecture.workflow_dag import (
    WORKFLOW_DAG_REGISTRY,
    get_workflow,
    get_workflows_for_pipeline,
    topological_order,
    check_workflow_dag_integrity,
    check_workflow_nodes_registered,
    check_workflow_gates_registered,
)
from zmatrix.architecture.skill_registry import SHARED_SKILL_REGISTRY
from zmatrix.architecture.pipeline_registry import PIPELINE_REGISTRY
from zmatrix.architecture.gate_registry import GATE_REGISTRY


def test_workflow_registry_exists():
    assert isinstance(WORKFLOW_DAG_REGISTRY, dict)
    assert len(WORKFLOW_DAG_REGISTRY) >= 2
    print(f"✅ workflow registry: {len(WORKFLOW_DAG_REGISTRY)} workflows")


def test_every_workflow_has_required_fields():
    for wid, w in WORKFLOW_DAG_REGISTRY.items():
        assert w.get("layer") == "workflow_dag"
        assert w.get("pipeline")
        assert w.get("purpose")
        assert w.get("nodes")
        assert w.get("edges")
        assert w.get("contract")
        assert w.get("test")
    print(f"✅ every workflow has required fields ({len(WORKFLOW_DAG_REGISTRY)} workflows)")


def test_workflow_pipeline_exists_in_registry():
    for wid, w in WORKFLOW_DAG_REGISTRY.items():
        assert w["pipeline"] in PIPELINE_REGISTRY, f"{wid}: pipeline '{w['pipeline']}' not registered"
    print("✅ all workflow pipelines exist in PIPELINE_REGISTRY")


def test_workflow_skill_nodes_registered():
    unreg = check_workflow_nodes_registered()
    assert len(unreg) == 0, f"unregistered nodes: {unreg}"
    print("✅ all workflow nodes exist in SHARED_SKILL_REGISTRY or GATE_REGISTRY")


def test_workflow_gates_registered():
    missing = check_workflow_gates_registered()
    assert len(missing) == 0, f"missing gates: {missing}"
    print("✅ all workflow required_gates exist in GATE_REGISTRY")


def test_no_cycles():
    for wid in WORKFLOW_DAG_REGISTRY:
        try:
            topological_order(wid)
        except ValueError as e:
            assert False, f"{wid}: {e}"
    print("✅ no workflow cycles detected")


def test_g18_workflow_contains_full_z9_chain():
    required = {"z9.sample.build", "z9.queue.build", "z9.backfill_task.build", "z9.calibration_policy.preview"}
    w = get_workflow("Z-G18.paper_z9_preview_workflow")
    assert w is not None
    nodes = set(w["nodes"])
    missing = required - nodes
    assert not missing, f"Z-G18 workflow missing: {missing}"
    print("✅ Z-G18 workflow: full Z9 preview chain present")


def test_rc_workflow_contains_all_steps():
    w = get_workflow("RC.release_verification_workflow")
    assert w is not None
    nodes = set(w["nodes"])
    for required in ["rc.checksum.build", "rc.packaging", "rc.verification", "safety.boundary_scan"]:
        assert required in nodes, f"RC workflow missing: {required}"
    print("✅ RC workflow: checksum + packaging + verification + safety present")


def test_topological_order():
    order = topological_order("Z-G18.paper_z9_preview_workflow")
    assert len(order) == 9
    assert order[0] == "r_matrix.evaluate_cycle"
    assert order[-1] == "z9.calibration_policy.preview"
    print(f"✅ topological_order: {order[0]} → ... → {order[-1]} (9 nodes)")


def test_workflow_integrity_clean():
    v = check_workflow_dag_integrity()
    assert len(v) == 0, f"integrity violations: {v}"
    print("✅ workflow DAG integrity clean")


def test_forbidden_capabilities_complete():
    for wid, w in WORKFLOW_DAG_REGISTRY.items():
        fc = w.get("forbidden_capabilities", [])
        for required in ["real_trade", "real_z9_write", "real_market_fetch", "auto_calibration"]:
            assert required in fc, f"{wid}: missing {required}"
    print("✅ all workflows forbid real_trade / real_z9_write / real_market_fetch / auto_calibration")


def test_get_workflow_api():
    assert get_workflow("Z-G18.paper_z9_preview_workflow") is not None
    assert get_workflow("nonexistent") is None
    print("✅ get_workflow API works")


def test_get_workflows_for_pipeline_api():
    g18_flows = get_workflows_for_pipeline("Z-G18")
    assert len(g18_flows) >= 1
    assert g18_flows[0][0] == "Z-G18.paper_z9_preview_workflow"
    print("✅ get_workflows_for_pipeline API works")


if __name__ == "__main__":
    test_workflow_registry_exists()
    test_every_workflow_has_required_fields()
    test_workflow_pipeline_exists_in_registry()
    test_workflow_skill_nodes_registered()
    test_workflow_gates_registered()
    test_no_cycles()
    test_g18_workflow_contains_full_z9_chain()
    test_rc_workflow_contains_all_steps()
    test_topological_order()
    test_workflow_integrity_clean()
    test_forbidden_capabilities_complete()
    test_get_workflow_api()
    test_get_workflows_for_pipeline_api()
    print("\n🏁 Workflow DAG v1.0 — all F-4 tests PASS")
