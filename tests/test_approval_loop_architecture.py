"""Approval Loop Architecture tests"""
import sys,os; sys.path.insert(0,os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pathlib import Path

def test_approval_skills_registered():
    from zmatrix.architecture.skill_registry import SHARED_SKILL_REGISTRY
    req = ["approval.request.build","approval.decision.build",
           "approval.policy.validate_request","approval.policy.validate_decision",
           "approval.queue.preview","approval.request_event.build","approval.human_event.build"]
    for s in req:
        assert s in SHARED_SKILL_REGISTRY, f"{s} missing"
    print(f"✅ {len(req)} Approval skills registered")

def test_approval_gates_registered():
    from zmatrix.architecture.gate_registry import GATE_REGISTRY
    for g in ["approval.request.valid","approval.decision.valid",
              "approval.no_auto_effect.valid","approval.human_required.valid"]:
        assert g in GATE_REGISTRY, f"{g} missing"
    print("✅ 4 Approval gates registered")

def test_approval_pipeline_registered():
    from zmatrix.architecture.pipeline_registry import PIPELINE_REGISTRY
    assert "Z-ApprovalReflectionLoop" in PIPELINE_REGISTRY
    p = PIPELINE_REGISTRY["Z-ApprovalReflectionLoop"]
    assert "hermes_memory_write" in p["forbidden_capabilities"]
    print("✅ Z-ApprovalReflectionLoop pipeline registered")

def test_approval_workflow_registered():
    from zmatrix.architecture.workflow_dag import WORKFLOW_DAG_REGISTRY
    wid = "Z-Approval.reflection_loop_workflow"
    assert wid in WORKFLOW_DAG_REGISTRY
    w = WORKFLOW_DAG_REGISTRY[wid]
    assert len(w["nodes"]) == 8
    assert "required_gates" in w
    print(f"✅ Approval workflow registered: {len(w['nodes'])} nodes")

def test_approval_workflow_required_gates():
    from zmatrix.architecture.workflow_dag import WORKFLOW_DAG_REGISTRY
    w = WORKFLOW_DAG_REGISTRY.get("Z-Approval.reflection_loop_workflow", {})
    req = ["approval.request.valid","approval.decision.valid",
           "approval.no_auto_effect.valid","approval.human_required.valid","safety.no_real_trade"]
    gates = w.get("required_gates", [])
    missing = [g for g in req if g not in gates]
    assert not missing, f"missing: {missing}"
    print(f"✅ workflow has {len(gates)} required gates")

def test_approval_docs_exist():
    root = Path(__file__).resolve().parent.parent
    docs = [
        "docs/contracts/APPROVAL_REQUEST_V10.md","docs/contracts/HUMAN_APPROVAL_DECISION_V10.md",
        "docs/contracts/APPROVAL_QUEUE_PREVIEW_V10.md","docs/contracts/APPROVAL_LOOP_V10.md",
        "docs/architecture/APPROVAL_REQUIRED_REFLECTION_LOOP_V10.md",
    ]
    for d in docs:
        assert (root / d).exists(), f"missing: {d}"
    print(f"✅ {len(docs)} Approval docs exist")

def test_approval_forbids_write_and_auto_ops():
    from zmatrix.architecture.pipeline_registry import PIPELINE_REGISTRY
    p = PIPELINE_REGISTRY.get("Z-ApprovalReflectionLoop", {})
    fc = p.get("forbidden_capabilities", [])
    assert "hermes_memory_write" in fc
    assert "auto_calibration" in fc
    assert "prompt_auto_injection" in fc
    print("✅ pipeline forbids auto ops")

if __name__ == "__main__":
    test_approval_skills_registered()
    test_approval_gates_registered()
    test_approval_pipeline_registered()
    test_approval_workflow_registered()
    test_approval_workflow_required_gates()
    test_approval_docs_exist()
    test_approval_forbids_write_and_auto_ops()
    print("\n🏁 Approval Loop Architecture tests PASS")
