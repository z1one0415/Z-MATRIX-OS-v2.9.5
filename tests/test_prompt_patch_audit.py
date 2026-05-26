"""Prompt Patch Audit tests"""
import sys, os; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from zmatrix.prompt_middleware.audit import build_prompt_patch_audit_record
from zmatrix.prompt_middleware.renderer import render_prompt_patch_preview
from zmatrix.prompt_middleware.patch_request import build_prompt_patch_request

def _make_audit():
    req = build_prompt_patch_request(task_context={}, prompt_patch_preview={"patch_id":"p"*32})
    render = render_prompt_patch_preview(prompt_patch_request=req)
    return build_prompt_patch_audit_record(prompt_patch_request=req, render_preview=render, audit_note="audit ok")

def test_prompt_patch_audit_blocks_runtime_effects():
    a = _make_audit()
    assert a["runtime_injection_allowed"] is False
    assert a["system_prompt_write_allowed"] is False
    assert a["hermes_memory_write_allowed"] is False
    print("✅ audit blocks runtime effects")

if __name__ == "__main__":
    test_prompt_patch_audit_blocks_runtime_effects()
    print("\n🏁 Prompt Patch Audit tests PASS")
