"""Prompt Middleware Policy tests"""
import sys, os; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from zmatrix.prompt_middleware.policy import (
    assert_no_prompt_runtime_effects,
    validate_prompt_patch_request,
)
from zmatrix.prompt_middleware.patch_request import build_prompt_patch_request

def test_policy_rejects_runtime_injection_true():
    record = {"runtime_injection_allowed": True}
    v = assert_no_prompt_runtime_effects(record)
    assert any("runtime_injection_allowed" in x for x in v)
    print("✅ policy rejects top-level runtime injection")

def test_policy_rejects_system_prompt_write_true():
    record = {"system_prompt_write_allowed": True}
    v = assert_no_prompt_runtime_effects(record)
    assert any("system_prompt_write_allowed" in x for x in v)
    print("✅ policy rejects top-level system_prompt write")

def test_policy_requires_rendered_prompt_preview():
    render = {"mode": "PREVIEW_ONLY", "render_status": "RENDERED_PREVIEW", "rendered_prompt_preview": ""}
    v = validate_prompt_render_preview(render)
    assert len(v) >= 1
    print("✅ policy requires rendered prompt preview")

# Need to import this for the test above
from zmatrix.prompt_middleware.policy import validate_prompt_render_preview

def test_valid_request_passes_policy():
    req = build_prompt_patch_request(
        task_context={"ticker": "002472"},
        prompt_patch_preview={"patch_id": "p" * 32},
    )
    v = validate_prompt_patch_request(req)
    assert v == [], f"expected 0 violations, got {v}"
    print("✅ valid request passes with 0 violations")

def test_policy_rejects_nested_safety_runtime_injection_true():
    record = {"safety": {"runtime_injection_allowed": True}}
    v = assert_no_prompt_runtime_effects(record)
    assert any("safety.runtime_injection_allowed" in x for x in v)
    print("✅ policy rejects nested safety.runtime_injection_allowed")

def test_policy_rejects_nested_safety_system_prompt_write_true():
    record = {"safety": {"system_prompt_write_allowed": True}}
    v = assert_no_prompt_runtime_effects(record)
    assert any("safety.system_prompt_write_allowed" in x for x in v)
    print("✅ policy rejects nested safety.system_prompt_write_allowed")

def test_policy_rejects_nested_safety_prompt_auto_injection_true():
    record = {"safety": {"prompt_auto_injection_allowed": True}}
    v = assert_no_prompt_runtime_effects(record)
    assert any("safety.prompt_auto_injection_allowed" in x for x in v)
    print("✅ policy rejects nested safety.prompt_auto_injection_allowed")

def test_policy_rejects_non_dict_safety():
    record = {"safety": "bad"}
    v = assert_no_prompt_runtime_effects(record)
    assert "safety must be dict" in v
    print("✅ policy rejects non-dict safety")

def test_approved_preview_with_nested_runtime_true_fails_policy():
    req = build_prompt_patch_request(
        task_context={"ticker": "002472"},
        prompt_patch_preview={"patch_id": "p" * 32},
        approval_decision={"approval_decision_id": "a" * 32, "result_status": "APPROVED"},
    )
    req["safety"]["runtime_injection_allowed"] = True
    v = validate_prompt_patch_request(req)
    assert any("safety.runtime_injection_allowed" in x for x in v)
    print("✅ APPROVED_PREVIEW + nested runtime_injection fails policy")

if __name__ == "__main__":
    test_policy_rejects_runtime_injection_true()
    test_policy_rejects_system_prompt_write_true()
    test_policy_requires_rendered_prompt_preview()
    test_valid_request_passes_policy()
    test_policy_rejects_nested_safety_runtime_injection_true()
    test_policy_rejects_nested_safety_system_prompt_write_true()
    test_policy_rejects_nested_safety_prompt_auto_injection_true()
    test_policy_rejects_non_dict_safety()
    test_approved_preview_with_nested_runtime_true_fails_policy()
    print("\n🏁 Prompt Middleware Policy tests PASS")
