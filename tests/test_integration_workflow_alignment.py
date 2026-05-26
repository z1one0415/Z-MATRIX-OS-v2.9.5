"""Workflow Alignment tests"""
import sys, os; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from zmatrix.integration.workflow_alignment import audit_workflow_alignment

def test_workflow_alignment_required_workflows_exist():
    r = audit_workflow_alignment()
    assert r["missing_workflows"] == []
    print("✅ all required workflows exist")

def test_workflow_alignment_required_gates_covered():
    r = audit_workflow_alignment()
    assert r["missing_gates"] == []
    print("✅ all required gates covered")

def test_workflow_edges_reference_existing_nodes():
    r = audit_workflow_alignment()
    assert r["node_violations"] == []
    assert r["edge_violations"] == []
    print("✅ all edges reference existing nodes")

def test_workflow_alignment_pipeline_gates_covered_by_workflow_gates():
    r = audit_workflow_alignment()
    assert r["gate_alignment_violations"] == []
    print("✅ pipeline gates covered by workflow gates")

def test_workflow_alignment_detects_missing_workflow_gate():
    from zmatrix.architecture import workflow_dag as wd
    wid = "Z-TailRisk.autonomic_gates_preview_workflow"
    original = list(wd.WORKFLOW_DAG_REGISTRY[wid]["required_gates"])
    wd.WORKFLOW_DAG_REGISTRY[wid]["required_gates"] = [g for g in original if g != "tail_risk.no_auto_sell.valid"]
    try:
        r = audit_workflow_alignment()
        assert r["pass"] is False
        assert r["gate_alignment_violations"]
    finally:
        wd.WORKFLOW_DAG_REGISTRY[wid]["required_gates"] = original
    print("✅ workflow alignment detects missing gate")

if __name__ == "__main__":
    test_workflow_alignment_required_workflows_exist()
    test_workflow_alignment_required_gates_covered()
    test_workflow_edges_reference_existing_nodes()
    test_workflow_alignment_pipeline_gates_covered_by_workflow_gates()
    test_workflow_alignment_detects_missing_workflow_gate()
    print("\n🏁 Workflow Alignment tests PASS")
