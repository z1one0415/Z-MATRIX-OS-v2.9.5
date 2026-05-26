"""Approval Event Adapters tests"""
import sys, os; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from zmatrix.approval_loop.event_adapters import build_approval_request_event, build_human_approval_event

def _req():
    return {"approval_request_id": "r1","request_version":"V10","request_type":"MEMORY_CANDIDATE_APPROVAL",
            "source_preview_id":"c1","requested_by":"test","status":"PENDING_REVIEW","requires_human_approval":True}

def _dec():
    return {"approval_decision_id":"d1","decision_version":"V10","approval_request_id":"r1",
            "decision":"APPROVE","result_status":"APPROVED","human_operator":"admin","rationale":"ok"}

def test_build_approval_request_event():
    e = build_approval_request_event(_req())
    assert e["event_type"] == "MemoryCandidateEvent"
    assert e["payload"]["status"] == "PENDING_REVIEW"
    assert e["safety"]["hermes_memory_write_allowed"] is False
    print("✅ build approval request event")

def test_build_human_approval_event():
    e = build_human_approval_event(_dec())
    assert e["event_type"] == "HumanApprovalEvent"
    assert e["payload"]["decision"] == "APPROVE"
    assert e["safety"]["real_z9_write_allowed"] is False
    print("✅ build human approval event")

def test_event_adapters_do_not_append():
    e = build_approval_request_event(_req())
    assert "stored" not in e
    print("✅ do not append")

if __name__ == "__main__":
    test_build_approval_request_event()
    test_build_human_approval_event()
    test_event_adapters_do_not_append()
    print("\n🏁 Approval Event Adapters tests PASS")
