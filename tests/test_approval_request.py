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

if __name__ == "__main__":
    test_approval_request_pending_review_only()
    test_approval_request_requires_human_approval()
    test_approval_request_blocks_auto_effects()
    print("\n🏁 Approval Request tests PASS")
