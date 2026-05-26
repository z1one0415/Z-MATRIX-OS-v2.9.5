"""CalibrationEvent Preview tests"""
import sys,os; sys.path.insert(0,os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from zmatrix.hermes_memory.calibration_event_preview import build_calibration_event_preview

def _make_candidate():
    return {"memory_candidate_id": "c"*32, "status": "DRAFT"}

def test_calibration_event_preview_only():
    r = build_calibration_event_preview(
        memory_candidate=_make_candidate(), target_domain="R_MATRIX", proposed_change={"weight": 0.1},
    )
    assert r["status"] == "PENDING_HUMAN_APPROVAL"
    print("✅ calibration event preview")

def test_calibration_event_requires_human_approval():
    r = build_calibration_event_preview(
        memory_candidate=_make_candidate(), target_domain="B_MATRIX", proposed_change={},
    )
    assert r["requires_human_approval"] is True
    print("✅ requires human approval")

def test_calibration_event_blocks_auto_apply():
    r = build_calibration_event_preview(
        memory_candidate=_make_candidate(), target_domain="Z8_POSITION_CONTROL", proposed_change={},
    )
    assert r["auto_apply_allowed"] is False
    print("✅ blocks auto apply")

def test_calibration_event_blocks_auto_calibration():
    r = build_calibration_event_preview(
        memory_candidate=_make_candidate(), target_domain="G18_DECISION", proposed_change={},
    )
    assert r["auto_calibration_allowed"] is False
    print("✅ blocks auto calibration")

def test_calibration_event_preserves_memory_candidate_link():
    cid = "candidate_" + "0"*24
    mc = {"memory_candidate_id": cid}
    r = build_calibration_event_preview(
        memory_candidate=mc, target_domain="UNKNOWN", proposed_change={},
    )
    assert r["memory_candidate_id"] == cid
    print("✅ preserves memory candidate link")

if __name__ == "__main__":
    test_calibration_event_preview_only()
    test_calibration_event_requires_human_approval()
    test_calibration_event_blocks_auto_apply()
    test_calibration_event_blocks_auto_calibration()
    test_calibration_event_preserves_memory_candidate_link()
    print("\n🏁 CalibrationEvent Preview tests PASS")
