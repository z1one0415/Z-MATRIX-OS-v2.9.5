"""Dry-Run Architecture tests"""
import sys,os; sys.path.insert(0,os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pathlib import Path

def test_dry_run_skills_registered():
    from zmatrix.architecture.skill_registry import SHARED_SKILL_REGISTRY
    for s in ["dry_run.rehearsal.build","dry_run.rehearsal.validate","dry_run.report.build"]:
        assert s in SHARED_SKILL_REGISTRY, f"{s} missing"
    print("✅ 3 Dry-run skills registered")

def test_dry_run_gates_registered():
    from zmatrix.architecture.gate_registry import GATE_REGISTRY
    for g in ["dry_run.only.valid","dry_run.no_runtime.valid","dry_run.no_real_trade.valid",
              "dry_run.no_memory_write.valid","dry_run.no_prompt_injection.valid"]:
        assert g in GATE_REGISTRY, f"{g} missing"
    print("✅ 5 Dry-run gates registered")

def test_dry_run_pipeline_registered():
    from zmatrix.architecture.pipeline_registry import PIPELINE_REGISTRY
    assert "Z-V3AlphaDryRunRehearsal" in PIPELINE_REGISTRY
    print("✅ Z-V3AlphaDryRunRehearsal pipeline registered")

def test_dry_run_workflow_registered():
    from zmatrix.architecture.workflow_dag import WORKFLOW_DAG_REGISTRY
    wid = "Z-DryRun.v3_alpha_rehearsal_workflow"
    assert wid in WORKFLOW_DAG_REGISTRY
    assert "required_gates" in WORKFLOW_DAG_REGISTRY[wid]
    print("✅ Dry-run workflow registered")

def test_dry_run_workflow_required_gates():
    from zmatrix.architecture.workflow_dag import WORKFLOW_DAG_REGISTRY
    w = WORKFLOW_DAG_REGISTRY.get("Z-DryRun.v3_alpha_rehearsal_workflow", {})
    req = ["dry_run.only.valid","dry_run.no_runtime.valid","dry_run.no_real_trade.valid",
           "dry_run.no_memory_write.valid","dry_run.no_prompt_injection.valid","safety.no_real_trade"]
    gates = w.get("required_gates", [])
    missing = [g for g in req if g not in gates]
    assert not missing, f"missing: {missing}"
    print(f"✅ workflow has {len(gates)} required gates")

def test_dry_run_docs_exist():
    root = Path(__file__).resolve().parent.parent
    docs = [
        "docs/contracts/V3_ALPHA_DRY_RUN_REHEARSAL_V10.md",
        "docs/contracts/V3_ALPHA_DRY_RUN_VALIDATION_V10.md",
        "docs/contracts/V3_ALPHA_DRY_RUN_REPORT_V10.md",
        "docs/architecture/V3_ALPHA_DRY_RUN_REHEARSAL_V10.md",
    ]
    for d in docs:
        assert (root / d).exists(), f"missing: {d}"
    print(f"✅ {len(docs)} Dry-run docs exist")

def test_dry_run_forbids_runtime_and_real_trade():
    from zmatrix.architecture.pipeline_registry import PIPELINE_REGISTRY
    p = PIPELINE_REGISTRY.get("Z-V3AlphaDryRunRehearsal", {})
    fc = p.get("forbidden_capabilities", [])
    assert "real_trade" in fc
    assert "runtime_prompt_injection" in fc
    assert "hermes_memory_write" in fc
    print("✅ pipeline forbids runtime, trade, hermes write")

if __name__ == "__main__":
    test_dry_run_skills_registered()
    test_dry_run_gates_registered()
    test_dry_run_pipeline_registered()
    test_dry_run_workflow_registered()
    test_dry_run_workflow_required_gates()
    test_dry_run_docs_exist()
    test_dry_run_forbids_runtime_and_real_trade()
    print("\n🏁 Dry-Run Architecture tests PASS")
