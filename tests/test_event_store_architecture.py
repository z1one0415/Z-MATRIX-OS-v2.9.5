"""EventStore architecture integration tests"""
import sys, os; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pathlib import Path

def test_event_store_skills_registered():
    from zmatrix.architecture.skill_registry import SHARED_SKILL_REGISTRY
    req = ["event_store.event.build", "event_store.local.append",
           "event_store.local.query", "event_store.lineage.trace",
           "event_store.jsonl.export"]
    for s in req:
        assert s in SHARED_SKILL_REGISTRY, f"{s} missing"
    print(f"✅ {len(req)} EventStore skills registered")

def test_event_store_gates_registered():
    from zmatrix.architecture.gate_registry import GATE_REGISTRY
    for g in ["event.schema.valid", "event.safety.valid",
              "event.lineage.valid", "event.append_only.valid"]:
        assert g in GATE_REGISTRY, f"{g} missing"
    print("✅ 4 EventStore gates registered")

def test_event_store_pipeline_registered():
    from zmatrix.architecture.pipeline_registry import PIPELINE_REGISTRY
    assert "Z-EventStore" in PIPELINE_REGISTRY
    p = PIPELINE_REGISTRY["Z-EventStore"]
    assert "hermes_memory_write" in p["forbidden_capabilities"]
    print("✅ Z-EventStore pipeline registered with Hermes write forbidden")

def test_event_store_workflow_registered():
    from zmatrix.architecture.workflow_dag import WORKFLOW_DAG_REGISTRY
    wid = "Z-EventStore.unified_event_ledger_workflow"
    assert wid in WORKFLOW_DAG_REGISTRY
    w = WORKFLOW_DAG_REGISTRY[wid]
    assert len(w["nodes"]) == 6
    assert len(w["edges"]) == 5
    print(f"✅ EventStore workflow registered: {len(w['nodes'])} nodes, {len(w['edges'])} edges")

def test_event_store_docs_exist():
    root = Path(__file__).resolve().parent.parent
    docs = [
        "docs/contracts/EVENT_STORE_V10.md",
        "docs/contracts/EVENT_SCHEMA_V10.md",
        "docs/contracts/EVENT_LINEAGE_V10.md",
        "docs/contracts/LOCAL_EVENT_STORE_V10.md",
        "docs/architecture/EVENT_STORE_ARCHITECTURE_V10.md",
    ]
    for d in docs:
        assert (root / d).exists(), f"missing: {d}"
    print(f"✅ {len(docs)} EventStore docs exist")

def test_event_store_forbids_real_z9_and_hermes_write():
    from zmatrix.architecture.pipeline_registry import PIPELINE_REGISTRY
    p = PIPELINE_REGISTRY.get("Z-EventStore", {})
    fc = p.get("forbidden_capabilities", [])
    assert "real_z9_write" in fc
    assert "hermes_memory_write" in fc
    print("✅ Z-EventStore pipeline forbids real_z9 and hermes_memory write")

if __name__ == "__main__":
    test_event_store_skills_registered()
    test_event_store_gates_registered()
    test_event_store_pipeline_registered()
    test_event_store_workflow_registered()
    test_event_store_docs_exist()
    test_event_store_forbids_real_z9_and_hermes_write()
    print("\n🏁 EventStore Architecture tests PASS")
