"""Alpha Tag Architecture tests"""
import sys,os; sys.path.insert(0,os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pathlib import Path

def test_alpha_tag_skills_registered():
    from zmatrix.architecture.skill_registry import SHARED_SKILL_REGISTRY
    for s in ["alpha_tag.artifact_consistency.validate","alpha_tag.tag_readiness.validate","alpha_tag.release_notes.build"]:
        assert s in SHARED_SKILL_REGISTRY, f"{s} missing"
    print("✅ 3 Alpha Tag skills registered")

def test_alpha_tag_gates_registered():
    from zmatrix.architecture.gate_registry import GATE_REGISTRY
    for g in ["alpha_tag.artifact_consistency.valid","alpha_tag.readiness.valid",
              "alpha_tag.no_git_tag_execute.valid","alpha_tag.no_git_push_tags.valid",
              "alpha_tag.no_runtime.valid","alpha_tag.no_real_trade.valid"]:
        assert g in GATE_REGISTRY, f"{g} missing"
    print("✅ 6 Alpha Tag gates registered")

def test_alpha_tag_pipeline_registered():
    from zmatrix.architecture.pipeline_registry import PIPELINE_REGISTRY
    assert "Z-V3AlphaFinalTagGate" in PIPELINE_REGISTRY
    print("✅ Z-V3AlphaFinalTagGate pipeline registered")

def test_alpha_tag_workflow_registered():
    from zmatrix.architecture.workflow_dag import WORKFLOW_DAG_REGISTRY
    wid = "Z-AlphaTag.final_tag_gate_workflow"
    assert wid in WORKFLOW_DAG_REGISTRY
    assert "required_gates" in WORKFLOW_DAG_REGISTRY[wid]
    print("✅ Alpha Tag workflow registered")

def test_alpha_tag_workflow_required_gates():
    from zmatrix.architecture.workflow_dag import WORKFLOW_DAG_REGISTRY
    w = WORKFLOW_DAG_REGISTRY.get("Z-AlphaTag.final_tag_gate_workflow", {})
    req = ["alpha_tag.artifact_consistency.valid","alpha_tag.readiness.valid",
           "alpha_tag.no_git_tag_execute.valid","alpha_tag.no_git_push_tags.valid",
           "alpha_tag.no_runtime.valid","alpha_tag.no_real_trade.valid","safety.no_real_trade"]
    gates = w.get("required_gates", [])
    missing = [g for g in req if g not in gates]
    assert not missing, f"missing: {missing}"
    print(f"✅ workflow has {len(gates)} required gates")

def test_alpha_tag_docs_exist():
    root = Path(__file__).resolve().parent.parent
    docs = [
        "docs/contracts/V3_ALPHA_ARTIFACT_CONSISTENCY_V10.md",
        "docs/contracts/V3_ALPHA_TAG_GATE_V10.md",
        "docs/contracts/V3_ALPHA_RC1_RELEASE_NOTES_V10.md",
        "docs/architecture/V3_ALPHA_FINAL_TAG_GATE_V10.md",
    ]
    for d in docs:
        assert (root / d).exists(), f"missing: {d}"
    print(f"✅ {len(docs)} Alpha Tag docs exist")

def test_alpha_tag_forbids_git_tag_and_runtime():
    from zmatrix.architecture.pipeline_registry import PIPELINE_REGISTRY
    p = PIPELINE_REGISTRY.get("Z-V3AlphaFinalTagGate", {})
    fc = p.get("forbidden_capabilities", [])
    assert "git_tag_execute" in fc
    assert "git_push_tags" in fc
    assert "runtime_prompt_injection" in fc
    print("✅ pipeline forbids git tag, git push, runtime")

if __name__ == "__main__":
    test_alpha_tag_skills_registered()
    test_alpha_tag_gates_registered()
    test_alpha_tag_pipeline_registered()
    test_alpha_tag_workflow_registered()
    test_alpha_tag_workflow_required_gates()
    test_alpha_tag_docs_exist()
    test_alpha_tag_forbids_git_tag_and_runtime()
    print("\n🏁 Alpha Tag Architecture tests PASS")
