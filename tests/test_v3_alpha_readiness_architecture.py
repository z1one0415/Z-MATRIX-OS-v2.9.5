"""v3.0-alpha Readiness Architecture tests"""
import sys,os; sys.path.insert(0,os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pathlib import Path

def test_v3_alpha_skills_registered():
    from zmatrix.architecture.skill_registry import SHARED_SKILL_REGISTRY
    req = ["integration.readiness_map.build","integration.capability_audit.run",
           "integration.workflow_alignment.audit","integration.event_chain.sample_build",
           "integration.event_chain.validate","integration.safety_matrix.build","integration.readiness_report.build"]
    for s in req:
        assert s in SHARED_SKILL_REGISTRY, f"{s} missing"
    print(f"✅ {len(req)} Integration skills registered")

def test_v3_alpha_gates_registered():
    from zmatrix.architecture.gate_registry import GATE_REGISTRY
    for g in ["integration.readiness_map.valid","integration.capability_audit.valid",
              "integration.workflow_alignment.valid","integration.event_chain.valid",
              "integration.safety_matrix.valid","integration.no_runtime_enable.valid"]:
        assert g in GATE_REGISTRY, f"{g} missing"
    print("✅ 6 Integration gates registered")

def test_v3_alpha_pipeline_registered():
    from zmatrix.architecture.pipeline_registry import PIPELINE_REGISTRY
    assert "Z-V3AlphaReadinessGate" in PIPELINE_REGISTRY
    print("✅ Z-V3AlphaReadinessGate pipeline registered")

def test_v3_alpha_workflow_registered():
    from zmatrix.architecture.workflow_dag import WORKFLOW_DAG_REGISTRY
    wid = "Z-Integration.v3_alpha_readiness_gate_workflow"
    assert wid in WORKFLOW_DAG_REGISTRY
    assert "required_gates" in WORKFLOW_DAG_REGISTRY[wid]
    print("✅ Integration workflow registered")

def test_v3_alpha_workflow_required_gates():
    from zmatrix.architecture.workflow_dag import WORKFLOW_DAG_REGISTRY
    w = WORKFLOW_DAG_REGISTRY.get("Z-Integration.v3_alpha_readiness_gate_workflow", {})
    req = ["integration.readiness_map.valid","integration.capability_audit.valid",
           "integration.workflow_alignment.valid","integration.event_chain.valid",
           "integration.safety_matrix.valid","integration.no_runtime_enable.valid","safety.no_real_trade"]
    gates = w.get("required_gates", [])
    missing = [g for g in req if g not in gates]
    assert not missing, f"missing: {missing}"
    print(f"✅ workflow has {len(gates)} required gates")

def test_v3_alpha_docs_exist():
    root = Path(__file__).resolve().parent.parent
    docs = [
        "docs/contracts/V3_ALPHA_READINESS_MAP_V10.md",
        "docs/contracts/FORBIDDEN_CAPABILITY_AUDIT_V10.md",
        "docs/contracts/WORKFLOW_ALIGNMENT_AUDIT_V10.md",
        "docs/contracts/V3_ALPHA_EVENT_CHAIN_SAMPLE_V10.md",
        "docs/contracts/CROSS_LAYER_SAFETY_MATRIX_V10.md",
        "docs/contracts/V3_ALPHA_READINESS_REPORT_V10.md",
        "docs/architecture/V3_ALPHA_INTEGRATION_READINESS_GATE_V10.md",
    ]
    for d in docs:
        assert (root / d).exists(), f"missing: {d}"
    print(f"✅ {len(docs)} Integration docs exist")

def test_v3_alpha_forbids_runtime_and_real_trade():
    from zmatrix.architecture.pipeline_registry import PIPELINE_REGISTRY
    p = PIPELINE_REGISTRY.get("Z-V3AlphaReadinessGate", {})
    fc = p.get("forbidden_capabilities", [])
    assert "real_trade" in fc
    assert "broker_order" in fc
    assert "hermes_memory_write" in fc
    assert "runtime_prompt_injection" in fc
    print("✅ pipeline forbids runtime, real trade, broker, hermes write")

if __name__ == "__main__":
    test_v3_alpha_skills_registered()
    test_v3_alpha_gates_registered()
    test_v3_alpha_pipeline_registered()
    test_v3_alpha_workflow_registered()
    test_v3_alpha_workflow_required_gates()
    test_v3_alpha_docs_exist()
    test_v3_alpha_forbids_runtime_and_real_trade()
    print("\n🏁 v3.0-alpha Readiness Architecture tests PASS")
