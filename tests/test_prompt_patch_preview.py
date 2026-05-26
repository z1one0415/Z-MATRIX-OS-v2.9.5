"""Prompt Patch Preview tests"""
import sys,os; sys.path.insert(0,os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from zmatrix.hermes_kernel.prompt_patch_preview import build_prompt_patch_preview

def _make_heuristic(status="ACTIVE", confidence="MEDIUM"):
    return {"title": f"heuristic-{status}", "confidence": confidence, "status": status, "rule": "observe", "scope": {}}

def test_prompt_patch_preview_is_preview_only():
    task = {"task_type": "stock_review", "ticker": "002472"}
    r = build_prompt_patch_preview(task_context=task, heuristics=[_make_heuristic()])
    assert r["mode"] == "PREVIEW_ONLY"
    assert r["injection_allowed"] is False
    print("✅ prompt patch preview-only")

def test_prompt_patch_requires_human_approval():
    r = build_prompt_patch_preview(task_context={"task_type":"test"}, heuristics=[])
    assert r["requires_human_approval"] is True
    print("✅ requires human approval")

def test_prompt_patch_blocks_auto_injection():
    r = build_prompt_patch_preview(task_context={"task_type":"test"}, heuristics=[])
    assert r["prompt_auto_injection_allowed"] is False
    print("✅ blocks auto injection")

def test_prompt_patch_redacts_forbidden_action_tokens():
    h = {"title": "BUY signal", "confidence": "HIGH", "status": "ACTIVE", "rule": "BUY when", "scope": {}}
    r = build_prompt_patch_preview(task_context={"task_type":"test"}, heuristics=[h])
    assert "BUY" not in r["prompt_patch_text"]
    assert "forbidden-action-token-redacted" in r["prompt_patch_text"]
    print("✅ redacts forbidden action tokens")

def test_prompt_patch_selects_active_heuristics_first():
    hs = [
        _make_heuristic(status="EXPIRED"),
        _make_heuristic(status="ACTIVE"),
        _make_heuristic(status="STALE"),
    ]
    r = build_prompt_patch_preview(task_context={"task_type":"test"}, heuristics=hs, max_items=2)
    # Should pick ACTIVE first
    assert r["selected_heuristics"][0]["status"] == "ACTIVE"
    print("✅ selects active heuristics first")

if __name__ == "__main__":
    test_prompt_patch_preview_is_preview_only()
    test_prompt_patch_requires_human_approval()
    test_prompt_patch_blocks_auto_injection()
    test_prompt_patch_redacts_forbidden_action_tokens()
    test_prompt_patch_selects_active_heuristics_first()
    print("\n🏁 Prompt Patch Preview tests PASS")
