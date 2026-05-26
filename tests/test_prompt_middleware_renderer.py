"""Prompt Middleware Renderer tests"""
import sys, os; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from zmatrix.prompt_middleware.renderer import render_prompt_patch_preview
from zmatrix.prompt_middleware.patch_request import build_prompt_patch_request

def _request():
    preview = {"patch_id": "p"*32, "prompt_patch_text": "Consider reviewing role context before decision"}
    return build_prompt_patch_request(task_context={"ticker":"002472"}, prompt_patch_preview=preview)

def test_render_preview_is_preview_only():
    r = render_prompt_patch_preview(prompt_patch_request=_request())
    assert r["mode"] == "PREVIEW_ONLY"
    assert r["render_status"] == "RENDERED_PREVIEW"
    print("✅ render preview is PREVIEW_ONLY")

def test_render_preview_does_not_write_system_prompt():
    r = render_prompt_patch_preview(prompt_patch_request=_request())
    assert r["system_prompt_write_allowed"] is False
    print("✅ render preview does not write system prompt")

def test_render_preview_blocks_runtime_injection():
    r = render_prompt_patch_preview(prompt_patch_request=_request())
    assert r["runtime_injection_allowed"] is False
    print("✅ render preview blocks runtime injection")

def test_rendered_prompt_contains_not_injected_banner():
    r = render_prompt_patch_preview(prompt_patch_request=_request())
    assert "NOT INJECTED" in r["rendered_prompt_preview"]
    print("✅ rendered prompt contains NOT INJECTED banner")

if __name__ == "__main__":
    test_render_preview_is_preview_only()
    test_render_preview_does_not_write_system_prompt()
    test_render_preview_blocks_runtime_injection()
    test_rendered_prompt_contains_not_injected_banner()
    print("\n🏁 Prompt Middleware Renderer tests PASS")
