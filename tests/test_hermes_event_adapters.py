"""Hermes Event Adapters tests — build only, no append"""
import sys,os; sys.path.insert(0,os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from zmatrix.hermes_memory.event_adapters import (
    build_memory_candidate_event, build_calibration_event, build_prompt_patch_event,
)

def _candidate():
    return {"memory_candidate_id":"c1","candidate_version":"V10","source_event_id":"a"*32,
            "mistake_type":"early_buy","severity":"LOW","confidence":"MEDIUM",
            "proposed_lesson":"wait","status":"DRAFT"}

def _calibration():
    return {"calibration_event_id":"cal1","calibration_version":"V10","memory_candidate_id":"c1",
            "target_domain":"R_MATRIX","proposed_change":{},"status":"PENDING_HUMAN_APPROVAL"}

def _patch():
    return {"patch_id":"p1","patch_version":"V10","task_context":{},"heuristic_count":0,"requires_human_approval":True}

def test_build_memory_candidate_event():
    e = build_memory_candidate_event(_candidate())
    assert e["event_type"] == "MemoryCandidateEvent"
    assert e["payload"]["status"] == "DRAFT"
    assert e["safety"]["hermes_memory_write_allowed"] is False
    print("✅ build memory candidate event")

def test_build_calibration_event():
    e = build_calibration_event(_calibration())
    assert e["event_type"] == "CalibrationEvent"
    assert e["payload"]["target_domain"] == "R_MATRIX"
    assert e["safety"]["real_z9_write_allowed"] is False
    print("✅ build calibration event")

def test_build_prompt_patch_event():
    e = build_prompt_patch_event(_patch())
    assert e["event_type"] == "PromptPatchEvent"
    assert e["payload"]["requires_human_approval"] is True
    print("✅ build prompt patch event")

def test_hermes_event_adapters_do_not_append():
    e = build_memory_candidate_event(_candidate())
    assert "stored" not in e
    print("✅ do not append")

def test_hermes_event_adapters_do_not_enable_memory_write():
    e = build_calibration_event(_calibration())
    assert e["safety"]["hermes_memory_write_allowed"] is False
    print("✅ do not enable memory write")

if __name__ == "__main__":
    test_build_memory_candidate_event()
    test_build_calibration_event()
    test_build_prompt_patch_event()
    test_hermes_event_adapters_do_not_append()
    test_hermes_event_adapters_do_not_enable_memory_write()
    print("\n🏁 Hermes Event Adapters tests PASS")
