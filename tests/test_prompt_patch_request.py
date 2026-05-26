"""Prompt Patch Request tests"""
import sys, os; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from zmatrix.prompt_middleware.patch_request import build_prompt_patch_request

def _preview():
    return {"patch_id": "p"*32, "prompt_patch_text": "test discipline"}

def _approval(result_status="APPROVED"):
    return {"approval_decision_id": "d"*32, "result_status": result_status}

def test_prompt_patch_request_pending_without_approval():
    r = build_prompt_patch_request(task_context={"ticker":"002472"}, prompt_patch_preview=_preview())
    assert r["approval_status"] == "PENDING_APPROVAL"
    assert r["status"] == "PENDING_APPROVAL"
    print("✅ request PENDING_APPROVAL without approval")

def test_prompt_patch_request_approved_preview_with_approval():
    r = build_prompt_patch_request(task_context={"ticker":"002472"}, prompt_patch_preview=_preview(), approval_decision=_approval())
    assert r["approval_status"] == "APPROVED_PREVIEW"
    assert r["status"] == "APPROVED_PREVIEW"
    print("✅ request APPROVED_PREVIEW with approval")

def test_approved_preview_does_not_enable_runtime_injection():
    r = build_prompt_patch_request(task_context={"ticker":"002472"}, prompt_patch_preview=_preview(), approval_decision=_approval())
    assert r["safety"]["runtime_injection_allowed"] is False
    print("✅ APPROVED_PREVIEW blocks runtime injection")

def test_prompt_patch_request_requires_preview_id():
    r = build_prompt_patch_request(task_context={"ticker":"002472"}, prompt_patch_preview=_preview())
    assert r["prompt_patch_preview_id"] == "p"*32
    print("✅ request has preview_id")

if __name__ == "__main__":
    test_prompt_patch_request_pending_without_approval()
    test_prompt_patch_request_approved_preview_with_approval()
    test_approved_preview_does_not_enable_runtime_injection()
    test_prompt_patch_request_requires_preview_id()
    print("\n🏁 Prompt Patch Request tests PASS")
