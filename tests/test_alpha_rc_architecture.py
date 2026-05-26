"""Alpha RC Architecture tests"""
import sys,os; sys.path.insert(0,os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pathlib import Path

def test_alpha_rc_skills_registered():
    from zmatrix.architecture.skill_registry import SHARED_SKILL_REGISTRY
    for s in ["alpha_rc.manifest.build","alpha_rc.verification_matrix.build",
              "alpha_rc.module_inventory.build","alpha_rc.known_limitations.build","alpha_rc.rc_gate.validate"]:
        assert s in SHARED_SKILL_REGISTRY, f"{s} missing"
    print("✅ 5 Alpha RC skills registered")

def test_alpha_rc_gates_registered():
    from zmatrix.architecture.gate_registry import GATE_REGISTRY
    for g in ["alpha_rc.manifest.valid","alpha_rc.verification_matrix.valid",
              "alpha_rc.module_inventory.valid","alpha_rc.known_limitations.valid",
              "alpha_rc.no_runtime.valid","alpha_rc.no_real_trade.valid"]:
        assert g in GATE_REGISTRY, f"{g} missing"
    print("✅ 6 Alpha RC gates registered")

def test_alpha_rc_pipeline_registered():
    from zmatrix.architecture.pipeline_registry import PIPELINE_REGISTRY
    assert "Z-V3AlphaRCPackaging" in PIPELINE_REGISTRY
    print("✅ Z-V3AlphaRCPackaging pipeline registered")

def test_alpha_rc_workflow_registered():
    from zmatrix.architecture.workflow_dag import WORKFLOW_DAG_REGISTRY
    wid = "Z-AlphaRC.packaging_freeze_workflow"
    assert wid in WORKFLOW_DAG_REGISTRY
    assert "required_gates" in WORKFLOW_DAG_REGISTRY[wid]
    print("✅ Alpha RC workflow registered")

def test_alpha_rc_workflow_required_gates():
    from zmatrix.architecture.workflow_dag import WORKFLOW_DAG_REGISTRY
    w = WORKFLOW_DAG_REGISTRY.get("Z-AlphaRC.packaging_freeze_workflow", {})
    req = ["alpha_rc.manifest.valid","alpha_rc.verification_matrix.valid",
           "alpha_rc.module_inventory.valid","alpha_rc.known_limitations.valid",
           "alpha_rc.no_runtime.valid","alpha_rc.no_real_trade.valid","safety.no_real_trade"]
    gates = w.get("required_gates", [])
    missing = [g for g in req if g not in gates]
    assert not missing, f"missing: {missing}"
    print(f"✅ workflow has {len(gates)} required gates")

def test_alpha_rc_docs_exist():
    root = Path(__file__).resolve().parent.parent
    docs = [
        "docs/contracts/V3_ALPHA_RELEASE_MANIFEST_V10.md",
        "docs/contracts/V3_ALPHA_VERIFICATION_MATRIX_V10.md",
        "docs/contracts/V3_ALPHA_FROZEN_MODULE_INVENTORY_V10.md",
        "docs/contracts/V3_ALPHA_KNOWN_LIMITATIONS_V10.md",
        "docs/contracts/V3_ALPHA_RC_GATE_VALIDATION_V10.md",
        "docs/architecture/V3_ALPHA_RC_PACKAGING_AND_FREEZE_V10.md",
    ]
    for d in docs:
        assert (root / d).exists(), f"missing: {d}"
    print(f"✅ {len(docs)} Alpha RC docs exist")

def test_alpha_rc_forbids_runtime_and_real_trade():
    from zmatrix.architecture.pipeline_registry import PIPELINE_REGISTRY
    p = PIPELINE_REGISTRY.get("Z-V3AlphaRCPackaging", {})
    fc = p.get("forbidden_capabilities", [])
    assert "real_trade" in fc
    assert "runtime_prompt_injection" in fc
    assert "hermes_memory_write" in fc
    print("✅ pipeline forbids runtime, trade, hermes write")

if __name__ == "__main__":
    test_alpha_rc_skills_registered()
    test_alpha_rc_gates_registered()
    test_alpha_rc_pipeline_registered()
    test_alpha_rc_workflow_registered()
    test_alpha_rc_workflow_required_gates()
    test_alpha_rc_docs_exist()
    test_alpha_rc_forbids_runtime_and_real_trade()
    print("\n🏁 Alpha RC Architecture tests PASS")
