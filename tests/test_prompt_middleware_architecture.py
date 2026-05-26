"""Prompt Middleware Architecture tests"""
import sys,os; sys.path.insert(0,os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pathlib import Path

def test_prompt_middleware_skills_registered():
    from zmatrix.architecture.skill_registry import SHARED_SKILL_REGISTRY
    req = ["prompt.patch_request.build","prompt.render_preview.build","prompt.audit.build",
           "prompt.policy.validate_request","prompt.policy.validate_render","prompt.policy.validate_audit",
           "prompt.patch_request_event.build","prompt.render_preview_event.build","prompt.audit_event.build"]
    for s in req:
        assert s in SHARED_SKILL_REGISTRY, f"{s} missing"
    print(f"✅ {len(req)} Prompt skills registered")

def test_prompt_middleware_gates_registered():
    from zmatrix.architecture.gate_registry import GATE_REGISTRY
    for g in ["prompt.preview_only.valid","prompt.no_runtime_injection.valid",
              "prompt.no_system_prompt_write.valid","prompt.no_auto_injection.valid","prompt.audit.valid"]:
        assert g in GATE_REGISTRY, f"{g} missing"
    print("✅ 5 Prompt gates registered")

def test_prompt_middleware_pipeline_registered():
    from zmatrix.architecture.pipeline_registry import PIPELINE_REGISTRY
    assert "Z-PromptMiddlewarePreview" in PIPELINE_REGISTRY
    p = PIPELINE_REGISTRY["Z-PromptMiddlewarePreview"]
    assert "runtime_prompt_injection" in p["forbidden_capabilities"]
    print("✅ Z-PromptMiddlewarePreview pipeline registered")

def test_prompt_middleware_workflow_registered():
    from zmatrix.architecture.workflow_dag import WORKFLOW_DAG_REGISTRY
    wid = "Z-Prompt.middleware_preview_workflow"
    assert wid in WORKFLOW_DAG_REGISTRY
    w = WORKFLOW_DAG_REGISTRY[wid]
    assert len(w["nodes"]) == 10
    assert "required_gates" in w
    print(f"✅ Prompt workflow registered: {len(w['nodes'])} nodes")

def test_prompt_middleware_workflow_required_gates():
    from zmatrix.architecture.workflow_dag import WORKFLOW_DAG_REGISTRY
    w = WORKFLOW_DAG_REGISTRY.get("Z-Prompt.middleware_preview_workflow", {})
    req = ["prompt.preview_only.valid","prompt.no_runtime_injection.valid",
           "prompt.no_system_prompt_write.valid","prompt.no_auto_injection.valid",
           "prompt.audit.valid","safety.no_real_trade"]
    gates = w.get("required_gates", [])
    missing = [g for g in req if g not in gates]
    assert not missing, f"missing: {missing}"
    print(f"✅ workflow has {len(gates)} required gates")

def test_prompt_middleware_docs_exist():
    root = Path(__file__).resolve().parent.parent
    docs = [
        "docs/contracts/PROMPT_PATCH_REQUEST_V10.md",
        "docs/contracts/PROMPT_MIDDLEWARE_RENDER_PREVIEW_V10.md",
        "docs/contracts/PROMPT_PATCH_AUDIT_V10.md",
        "docs/contracts/PROMPT_MIDDLEWARE_V10.md",
        "docs/architecture/PROMPT_HOT_PATCHING_MIDDLEWARE_PREVIEW_V10.md",
    ]
    for d in docs:
        assert (root / d).exists(), f"missing: {d}"
    print(f"✅ {len(docs)} Prompt docs exist")

def test_prompt_middleware_forbids_runtime_injection_and_prompt_write():
    from zmatrix.architecture.pipeline_registry import PIPELINE_REGISTRY
    p = PIPELINE_REGISTRY.get("Z-PromptMiddlewarePreview", {})
    fc = p.get("forbidden_capabilities", [])
    assert "runtime_prompt_injection" in fc
    assert "system_prompt_write" in fc
    assert "prompt_auto_injection" in fc
    print("✅ pipeline forbids runtime injection, system prompt write, auto injection")

if __name__ == "__main__":
    test_prompt_middleware_skills_registered()
    test_prompt_middleware_gates_registered()
    test_prompt_middleware_pipeline_registered()
    test_prompt_middleware_workflow_registered()
    test_prompt_middleware_workflow_required_gates()
    test_prompt_middleware_docs_exist()
    test_prompt_middleware_forbids_runtime_injection_and_prompt_write()
    print("\n🏁 Prompt Middleware Architecture tests PASS")
