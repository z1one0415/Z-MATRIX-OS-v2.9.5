"""Working Context tests"""
import sys,os; sys.path.insert(0,os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from zmatrix.hermes_kernel.working_context import build_working_context_from_events

def test_working_context_read_only():
    events = [{"event_id": "a"*32, "event_type": "ResearchEvent", "payload": {"ticker": "002472"}}]
    r = build_working_context_from_events(events=events, ticker="002472", role="A_LONG_CORE")
    assert r["preview_only"] is True
    assert r["write_allowed"] is False
    assert r["hermes_memory_write_allowed"] is False
    print("✅ working context read-only")

def test_working_context_extracts_events():
    events = [
        {"event_id": "a"*32, "event_type": "OutcomeBackfillEvent", "payload": {}},
        {"event_id": "b"*32, "event_type": "PaperLedgerEvent", "payload": {}},
    ]
    r = build_working_context_from_events(events=events, ticker="002472")
    assert len(r["extracted_outcomes"]) == 1
    assert len(r["extracted_papers"]) == 1
    print("✅ working context extracts events")

if __name__ == "__main__":
    test_working_context_read_only()
    test_working_context_extracts_events()
    print("\n🏁 Working Context tests PASS")
