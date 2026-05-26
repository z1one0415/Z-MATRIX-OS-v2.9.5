"""Workflow Alignment tests"""
import sys, os; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from zmatrix.integration.workflow_alignment import audit_workflow_alignment

def test_workflow_alignment_required_workflows_exist():
    r = audit_workflow_alignment()
    assert len(r["missing_workflows"]) == 0
    print("✅ all required workflows exist")

def test_workflow_alignment_required_gates_covered():
    r = audit_workflow_alignment()
    assert len(r["missing_gates"]) == 0
    print("✅ all required gates covered")

def test_workflow_edges_reference_existing_nodes():
    r = audit_workflow_alignment()
    assert len(r["edge_violations"]) == 0
    print("✅ all edges reference existing nodes")

if __name__ == "__main__":
    test_workflow_alignment_required_workflows_exist()
    test_workflow_alignment_required_gates_covered()
    test_workflow_edges_reference_existing_nodes()
    print("\n🏁 Workflow Alignment tests PASS")
