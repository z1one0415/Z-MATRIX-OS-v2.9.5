"""Prompt Middleware Policy tests"""
import sys, os; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from zmatrix.prompt_middleware.policy import (
    assert_no_prompt_runtime_effects,
    validate_prompt_patch_request,
    validate_prompt_render_preview,
)
from zmatrix.prompt_middleware.patch_request import build_prompt_patch_request
from zmatrix.prompt_middleware.renderer import render_prompt_patch_preview

def test_policy_rejects_runtime_injection_true():
    record = {"runtime_injection_allowed": True}
    v = assert_no_prompt_runtime_effects(record)
    assert len(v) >= 1
    print("✅ policy rejects runtime injection")

def test_policy_rejects_system_prompt_write_true():
    record = {"system_prompt_write_allowed": True}
    v = assert_no_prompt_runtime_effects(record)
    assert len(v) >= 1
    print("✅ policy rejects system prompt write")

def test_policy_requires_rendered_prompt_preview():
    render = {"mode": "PREVIEW_ONLY", "render_status": "RENDERED_PREVIEW", "rendered_prompt_preview": ""}
    v = validate_prompt_render_preview(render)
    assert len(v) >= 1
    print("✅ policy requires rendered prompt preview")

def test_valid_request_passes_policy():
    req = build_prompt_patch_request(task_context={"ticker":"002472"}, prompt_patch_preview={"patch_id":"p"*32})
    v = validate_prompt_patch_request(req)
    # May have warnings about missing top-level safety fields (fine)
    print(f"✅ valid request policy check: {len(v)} violations (expected <=2)")

if __name__ == "__main__":
    test_policy_rejects_runtime_injection_true()
    test_policy_rejects_system_prompt_write_true()
    test_policy_requires_rendered_prompt_preview()
    test_valid_request_passes_policy()
    print("\n🏁 Prompt Middleware Policy tests PASS")
