"""Approval Request tests"""
import sys, os; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from zmatrix.approval_loop.approval_request import build_approval_request

def _preview():
    return {"candidate_id": "c"*32, "source_event_id": "a"*32}

def test_approval_request_pending_review_only():
    r = build_approval_request(request_type="MEMORY_CANDIDATE_APPROVAL", source_preview=_preview())
    assert r["status"] == "PENDING_REVIEW"
    print("✅ approval request PENDING_REVIEW")

def test_approval_request_requires_human_approval():
    r = build_approval_request(request_type="MEMORY_CANDIDATE_APPROVAL", source_preview=_preview())
    assert r["requires_human_approval"] is True
    print("✅ requires human approval")

def test_approval_request_blocks_auto_effects():
    r = build_approval_request(request_type="MEMORY_CANDIDATE_APPROVAL", source_preview=_preview())
    assert r["safety"]["hermes_memory_write_allowed"] is False
    assert r["safety"]["real_z9_write_allowed"] is False
    assert r["safety"]["auto_calibration_allowed"] is False
    assert r["safety"]["prompt_auto_injection_allowed"] is False
    print("✅ blocks auto effects")

def test_approval_request_extracts_calibration_event_id():
    source_preview = {"calibration_event_id": "c" * 32, "target_domain": "R_MATRIX"}
    r = build_approval_request(request_type="CALIBRATION_EVENT_APPROVAL", source_preview=source_preview, reason="review calibration")
    assert r["source_preview_id"] == "c" * 32
    assert r["source_preview_hash"]
    assert r["status"] == "PENDING_REVIEW"
    print("✅ extracts calibration_event_id")

def test_approval_request_ids_differ_for_different_source_previews_without_source_event_id():
    r1 = build_approval_request(request_type="PROMPT_PATCH_APPROVAL", source_preview={"patch_id": "p1", "content": "a"}, reason="review")
    r2 = build_approval_request(request_type="PROMPT_PATCH_APPROVAL", source_preview={"patch_id": "p2", "content": "b"}, reason="review")
    assert r1["approval_request_id"] != r2["approval_request_id"]
    print("✅ different source_previews produce different request_ids")

if __name__ == "__main__":
    test_approval_request_pending_review_only()
    test_approval_request_requires_human_approval()
    test_approval_request_blocks_auto_effects()
    test_approval_request_extracts_calibration_event_id()
    test_approval_request_ids_differ_for_different_source_previews_without_source_event_id()
    print("\n🏁 Approval Request tests PASS")
