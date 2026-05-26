"""Approval Decision tests"""
import sys, os; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from zmatrix.approval_loop.approval_decision import build_human_approval_decision

def _request():
    return {"approval_request_id": "req" + "0"*29, "source_preview_id": "c"*32}

def test_human_approval_decision_approve_maps_to_approved():
    d = build_human_approval_decision(approval_request=_request(), decision="APPROVE", human_operator="admin", rationale="ok")
    assert d["decision"] == "APPROVE"
    assert d["result_status"] == "APPROVED"
    print("✅ APPROVE → APPROVED")

def test_human_approval_decision_reject_maps_to_rejected():
    d = build_human_approval_decision(approval_request=_request(), decision="REJECT", human_operator="admin", rationale="no")
    assert d["decision"] == "REJECT"
    assert d["result_status"] == "REJECTED"
    print("✅ REJECT → REJECTED")

def test_human_approval_decision_quarantine_maps_to_quarantined():
    d = build_human_approval_decision(approval_request=_request(), decision="QUARANTINE", human_operator="admin", rationale="suspect")
    assert d["result_status"] == "QUARANTINED"
    print("✅ QUARANTINE → QUARANTINED")

def test_approve_does_not_enable_hermes_write():
    d = build_human_approval_decision(approval_request=_request(), decision="APPROVE", human_operator="admin", rationale="ok")
    assert d["safety"]["hermes_memory_write_allowed"] is False
    print("✅ APPROVE does not enable Hermes write")

def test_approve_does_not_enable_auto_calibration():
    d = build_human_approval_decision(approval_request=_request(), decision="APPROVE", human_operator="admin", rationale="ok")
    assert d["safety"]["auto_calibration_allowed"] is False
    print("✅ APPROVE does not enable auto calibration")

def test_approve_does_not_enable_prompt_injection():
    d = build_human_approval_decision(approval_request=_request(), decision="APPROVE", human_operator="admin", rationale="ok")
    assert d["safety"]["prompt_auto_injection_allowed"] is False
    print("✅ APPROVE does not enable prompt injection")

if __name__ == "__main__":
    test_human_approval_decision_approve_maps_to_approved()
    test_human_approval_decision_reject_maps_to_rejected()
    test_human_approval_decision_quarantine_maps_to_quarantined()
    test_approve_does_not_enable_hermes_write()
    test_approve_does_not_enable_auto_calibration()
    test_approve_does_not_enable_prompt_injection()
    print("\n🏁 Approval Decision tests PASS")
