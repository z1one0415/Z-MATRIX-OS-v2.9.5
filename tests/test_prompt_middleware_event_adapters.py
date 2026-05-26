"""Prompt Middleware Event Adapters tests"""
import sys, os; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from zmatrix.prompt_middleware.event_adapters import (
    build_prompt_patch_request_event,
    build_prompt_render_preview_event,
    build_prompt_patch_audit_event,
)

def _req():
    return {"prompt_patch_request_id":"r1","request_version":"V10","request_type":"TASK_DISCIPLINE_PATCH",
            "approval_status":"PENDING_APPROVAL","status":"PENDING_APPROVAL"}
def _render():
    return {"render_id":"r1","render_version":"V10","mode":"PREVIEW_ONLY","render_status":"RENDERED_PREVIEW"}
def _audit():
    return {"prompt_patch_audit_id":"a1","audit_version":"V10","audit_status":"PREVIEW_AUDITED"}

def test_build_prompt_patch_request_event():
    e = build_prompt_patch_request_event(_req())
    assert e["event_type"] == "PromptPatchEvent"
    assert e["payload"]["event_subtype"] == "PromptPatchRequest"
    assert e["safety"]["hermes_memory_write_allowed"] is False
    print("✅ build prompt patch request event")

def test_build_prompt_render_preview_event():
    e = build_prompt_render_preview_event(_render())
    assert e["event_type"] == "PromptPatchEvent"
    assert e["payload"]["event_subtype"] == "PromptRenderPreview"
    print("✅ build render preview event")

def test_build_prompt_patch_audit_event():
    e = build_prompt_patch_audit_event(_audit())
    assert e["event_type"] == "PromptPatchEvent"
    assert e["payload"]["event_subtype"] == "PromptPatchAudit"
    print("✅ build audit event")

def test_event_adapters_do_not_append():
    e = build_prompt_patch_request_event(_req())
    assert "stored" not in e
    print("✅ do not append")

if __name__ == "__main__":
    test_build_prompt_patch_request_event()
    test_build_prompt_render_preview_event()
    test_build_prompt_patch_audit_event()
    test_event_adapters_do_not_append()
    print("\n🏁 Prompt Middleware Event Adapters tests PASS")
