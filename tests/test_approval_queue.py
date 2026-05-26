"""Approval Queue tests"""
import sys, os; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from zmatrix.approval_loop.approval_queue import build_approval_queue_preview

def test_queue_preview_is_not_auto_processed():
    q = build_approval_queue_preview([])
    assert q["auto_process_allowed"] is False
    print("✅ queue not auto processed")

def test_queue_requires_human_review():
    q = build_approval_queue_preview([])
    assert q["requires_human_review"] is True
    print("✅ queue requires human review")

def test_queue_prioritizes_high_severity():
    requests = [
        {"status": "PENDING_REVIEW", "request_type": "MEMORY_CANDIDATE_APPROVAL",
         "source_preview": {"severity": "LOW"}},
        {"status": "PENDING_REVIEW", "request_type": "MEMORY_CANDIDATE_APPROVAL",
         "source_preview": {"severity": "HIGH"}},
    ]
    q = build_approval_queue_preview(requests)
    assert q["pending_count"] == 2
    assert q["requests"][0]["source_preview"]["severity"] == "HIGH"
    print("✅ queue prioritizes HIGH severity")

if __name__ == "__main__":
    test_queue_preview_is_not_auto_processed()
    test_queue_requires_human_review()
    test_queue_prioritizes_high_severity()
    print("\n🏁 Approval Queue tests PASS")
