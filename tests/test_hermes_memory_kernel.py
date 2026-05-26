"""Hermes Memory Kernel tests"""
import sys,os; sys.path.insert(0,os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from zmatrix.hermes_memory.hermes_memory_kernel import build_hermes_memory_kernel_preview

def test_kernel_is_read_only_preview():
    r = build_hermes_memory_kernel_preview(task_context={"task_type":"stock_review","ticker":"002472"})
    assert r["mode"] == "READ_ONLY_PREVIEW"
    assert r["write_allowed"] is False
    print("✅ kernel read-only preview")

def test_kernel_blocks_hermes_memory_write():
    r = build_hermes_memory_kernel_preview(task_context={"task_type":"outcome_review","ticker":"601899"})
    assert r["hermes_memory_write_allowed"] is False
    print("✅ blocks hermes memory write")

def test_kernel_blocks_prompt_auto_injection():
    r = build_hermes_memory_kernel_preview(task_context={"task_type":"test"})
    assert r["prompt_auto_injection_allowed"] is False
    print("✅ blocks prompt auto injection")

def test_kernel_builds_prompt_patch_preview():
    heuristics = [{"title":"h1","confidence":"MEDIUM","status":"ACTIVE","rule":"observe","scope":{}}]
    r = build_hermes_memory_kernel_preview(
        task_context={"task_type":"paper_decision","ticker":"002472"},
        learned_heuristics=heuristics,
    )
    pp = r.get("prompt_patch_preview", {})
    assert pp.get("mode") == "PREVIEW_ONLY"
    assert pp.get("prompt_auto_injection_allowed") is False
    print("✅ builds prompt patch preview")

def test_kernel_does_not_append_event_store():
    r = build_hermes_memory_kernel_preview(task_context={"task_type":"test"})
    assert "event_id" not in r
    print("✅ does not append event store")

if __name__ == "__main__":
    test_kernel_is_read_only_preview()
    test_kernel_blocks_hermes_memory_write()
    test_kernel_blocks_prompt_auto_injection()
    test_kernel_builds_prompt_patch_preview()
    test_kernel_does_not_append_event_store()
    print("\n🏁 Hermes Memory Kernel tests PASS")
