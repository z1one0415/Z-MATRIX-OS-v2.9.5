"""Event Adapter tests"""
import sys,os; sys.path.insert(0,'.')
from zmatrix.paper_outcome.event_adapter import build_outcome_event

def test_build_outcome_event():
    e = build_outcome_event({"outcome_id":"o1","paper_id":"p1","ticker":"002472","outcome_status":"READY"})
    assert e["event_type"] == "OutcomeBackfillEvent"
    assert e["payload"]["ticker"] == "002472"
    assert "stored" not in e
    print("✅ build event, no append")

if __name__ == "__main__":
    test_build_outcome_event()
    print("\n🏁 Event Adapter PASS")
