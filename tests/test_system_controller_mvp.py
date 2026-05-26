"""System Controller MVP tests"""
import sys,os; sys.path.insert(0,os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from zmatrix.architecture.system_controller import build_system_execution_plan

def test_ordered_nodes_contains_full_z9_chain():
    plan = build_system_execution_plan("Z-G18.paper_z9_preview_workflow")
    nodes = plan["ordered_nodes"]
    assert "z9.sample.build" in nodes
    assert "z9.queue.build" in nodes
    assert "z9.backfill_task.build" in nodes
    assert "z9.calibration_policy.preview" in nodes
    assert nodes[-1] == "z9.calibration_policy.preview"
    assert nodes[0] is not None
    print(f"✅ plan: ordered_nodes ({len(nodes)} nodes) with full Z9 chain")

def test_missing_workflow_rejected():
    plan = build_system_execution_plan("nonexistent")
    assert plan["reason"] == "WORKFLOW_NOT_FOUND"
    print("✅ plan: missing workflow rejected")

def test_no_runtime_execution():
    plan = build_system_execution_plan("Z-G18.paper_z9_preview_workflow")
    assert "empty G18" not in str(plan)
    assert plan["validation"]["ready_for_runtime"] is False
    assert plan["reason"] == "SYSTEM_CONTROLLER_MVP_PLAN_ONLY_NO_RUNTIME_EXECUTION"
    print("✅ plan: no runtime execution, plan only")

def test_all_gates_registered():
    plan = build_system_execution_plan("Z-G18.paper_z9_preview_workflow")
    assert plan["validation"]["gates_registered"] is True
    actual_gates = set(plan["required_gates"])
    # The exact set may vary as new gates are added; just check key gates present
    assert "safety.no_real_trade" in actual_gates
    assert len(actual_gates) >= 3
    print(f"✅ plan: {len(actual_gates)} gates registered ({' '.join(sorted(actual_gates))})")

def test_rc_workflow_plan():
    plan = build_system_execution_plan("RC.release_verification_workflow")
    assert plan["pipeline_id"] == "RC-release"
    assert "rc.checksum.build" in plan["ordered_nodes"]
    assert plan["execution_allowed"] is False
    print("✅ plan: RC workflow plan (checksum/packaging/verification/safety)")

def test_execution_flag_always_false():
    plan = build_system_execution_plan("Z-EventStore.unified_event_ledger_workflow")
    assert plan["execution_allowed"] is False
    assert plan["real_ops_allowed"] is False
    assert plan["validation"]["ready_for_runtime"] is False
    print("✅ plan: EventStore workflow plan (execution blocked)")

def test_event_store_workflow_plan():
    plan = build_system_execution_plan("Z-EventStore.unified_event_ledger_workflow")
    assert plan["pipeline_id"] == "Z-EventStore"
    assert "event_store.event.build" in plan["ordered_nodes"]
    assert plan["validation"]["workflow_exists"] is True
    print(f"✅ plan: EventStore workflow ({len(plan['ordered_nodes'])} nodes)")

if __name__ == "__main__":
    test_ordered_nodes_contains_full_z9_chain()
    test_missing_workflow_rejected()
    test_no_runtime_execution()
    test_all_gates_registered()
    test_rc_workflow_plan()
    test_execution_flag_always_false()
    test_event_store_workflow_plan()
    print("\n🏁 System Controller MVP — tests PASS")
