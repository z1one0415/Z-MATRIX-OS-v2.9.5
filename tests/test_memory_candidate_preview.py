"""MemoryCandidate Preview tests"""
import sys,os; sys.path.insert(0,os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from zmatrix.hermes_memory.memory_candidate_preview import build_memory_candidate_preview

def _source_event(event_id="a"*32):
    return {"event_id": event_id, "event_type": "OutcomeBackfillEvent", "payload": {}}

def test_memory_candidate_preview_draft_only():
    r = build_memory_candidate_preview(
        source_event=_source_event(), attribution={"mistake_type":"early_buy","severity":"MEDIUM"},
        proposed_lesson="wait for confirmation",
    )
    assert r["status"] == "DRAFT"
    print("✅ memory candidate is DRAFT")

def test_memory_candidate_requires_human_approval():
    r = build_memory_candidate_preview(
        source_event=_source_event(), attribution={"mistake_type":"late_sell"},
        proposed_lesson="hold longer",
    )
    assert r["requires_human_approval"] is True
    print("✅ requires human approval")

def test_memory_candidate_does_not_write_hermes():
    r = build_memory_candidate_preview(
        source_event=_source_event(), attribution={},
        proposed_lesson="observe",
    )
    assert r["hermes_memory_write_allowed"] is False
    print("✅ does not write hermes")

def test_memory_candidate_does_not_auto_calibrate():
    r = build_memory_candidate_preview(
        source_event=_source_event(), attribution={},
        proposed_lesson="observe",
    )
    assert r["auto_calibration_allowed"] is False
    print("✅ does not auto calibrate")

def test_memory_candidate_links_source_event():
    eid = "abc123" + "0"*26
    r = build_memory_candidate_preview(
        source_event=_source_event(event_id=eid), attribution={"mistake_type":"risk_violation"},
        proposed_lesson="check risk first",
    )
    assert r["source_event_id"] == eid
    print("✅ links source event")

if __name__ == "__main__":
    test_memory_candidate_preview_draft_only()
    test_memory_candidate_requires_human_approval()
    test_memory_candidate_does_not_write_hermes()
    test_memory_candidate_does_not_auto_calibrate()
    test_memory_candidate_links_source_event()
    print("\n🏁 MemoryCandidate Preview tests PASS")
