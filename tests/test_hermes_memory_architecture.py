"""Hermes Memory Kernel Architecture tests"""
import sys,os; sys.path.insert(0,os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pathlib import Path

def test_hermes_memory_skills_registered():
    from zmatrix.architecture.skill_registry import SHARED_SKILL_REGISTRY
    req = ["hermes.core_memory.load","hermes.working_context.build","hermes.heuristics.retrieve",
           "hermes.prompt_patch.preview","hermes.memory_candidate.preview",
           "hermes.calibration_event.preview","hermes.memory_kernel.preview",
           "hermes.memory_candidate_event.build","hermes.calibration_event.build",
           "hermes.prompt_patch_event.build"]
    for s in req:
        assert s in SHARED_SKILL_REGISTRY, f"{s} missing"
    print(f"✅ {len(req)} Hermes skills registered")

def test_hermes_memory_gates_registered():
    from zmatrix.architecture.gate_registry import GATE_REGISTRY
    for g in ["hermes.read_only.valid","hermes.preview_only.valid","hermes.no_memory_write.valid",
              "hermes.no_auto_calibration.valid","hermes.no_prompt_auto_injection.valid"]:
        assert g in GATE_REGISTRY, f"{g} missing"
    print("✅ 5 Hermes gates registered")

def test_hermes_memory_pipeline_registered():
    from zmatrix.architecture.pipeline_registry import PIPELINE_REGISTRY
    assert "Z-HermesMemoryKernel" in PIPELINE_REGISTRY
    p = PIPELINE_REGISTRY["Z-HermesMemoryKernel"]
    assert "hermes_memory_write" in p["forbidden_capabilities"]
    print("✅ Z-HermesMemoryKernel pipeline registered")

def test_hermes_memory_workflow_registered():
    from zmatrix.architecture.workflow_dag import WORKFLOW_DAG_REGISTRY
    wid = "Z-Hermes.memory_kernel_preview_workflow"
    assert wid in WORKFLOW_DAG_REGISTRY
    w = WORKFLOW_DAG_REGISTRY[wid]
    assert len(w["nodes"]) == 11
    assert "required_gates" in w
    print(f"✅ Hermes workflow registered: {len(w['nodes'])} nodes")

def test_hermes_memory_docs_exist():
    root = Path(__file__).resolve().parent.parent
    docs = [
        "docs/contracts/CORE_MEMORY_V10.md","docs/contracts/WORKING_CONTEXT_V10.md",
        "docs/contracts/LEARNED_HEURISTICS_V10.md","docs/contracts/PROMPT_PATCH_PREVIEW_V10.md",
        "docs/contracts/MEMORY_CANDIDATE_PREVIEW_V10.md","docs/contracts/CALIBRATION_EVENT_PREVIEW_V10.md",
        "docs/contracts/HERMES_MEMORY_KERNEL_V10.md","docs/architecture/HERMES_MEMORY_KERNEL_ARCHITECTURE_V10.md",
    ]
    for d in docs:
        assert (root / d).exists(), f"missing: {d}"
    print(f"✅ {len(docs)} Hermes docs exist")

def test_hermes_memory_forbids_write_and_auto_ops():
    from zmatrix.architecture.pipeline_registry import PIPELINE_REGISTRY
    p = PIPELINE_REGISTRY.get("Z-HermesMemoryKernel", {})
    fc = p.get("forbidden_capabilities", [])
    assert "hermes_memory_write" in fc
    assert "real_z9_write" in fc
    assert "auto_calibration" in fc
    assert "prompt_auto_injection" in fc
    print("✅ pipeline forbids hermes write, Z9 write, auto calibration, prompt injection")

def test_hermes_workflow_required_gates():
    from zmatrix.architecture.workflow_dag import WORKFLOW_DAG_REGISTRY
    w = WORKFLOW_DAG_REGISTRY.get("Z-Hermes.memory_kernel_preview_workflow", {})
    req = ["hermes.read_only.valid","hermes.preview_only.valid","hermes.no_memory_write.valid",
           "hermes.no_auto_calibration.valid","hermes.no_prompt_auto_injection.valid","safety.no_real_trade"]
    gates = w.get("required_gates", [])
    missing = [g for g in req if g not in gates]
    assert not missing, f"missing: {missing}"
    print(f"✅ workflow has {len(gates)} required gates (all present)")

if __name__ == "__main__":
    test_hermes_memory_skills_registered()
    test_hermes_memory_gates_registered()
    test_hermes_memory_pipeline_registered()
    test_hermes_memory_workflow_registered()
    test_hermes_memory_docs_exist()
    test_hermes_memory_forbids_write_and_auto_ops()
    test_hermes_workflow_required_gates()
    print("\n🏁 Hermes Memory Architecture tests PASS")
