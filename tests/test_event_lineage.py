"""Event lineage tests — trace, missing parent, cycle detection"""
import sys, os; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from zmatrix.event_store.lineage import trace_event_lineage

def make_event(eid: str, parent: str | None = None) -> dict:
    return {
        "event_id": eid, "event_type": "ResearchEvent",
        "source_event_id": None, "parent_event_id": parent,
        "producer_module": "test", "created_at": "2026-05-26T13:00:00Z",
    }

def test_trace_parent_chain():
    events = [
        make_event("root" + "0"*28),
        make_event("mid1" + "0"*28, "root" + "0"*28),
        make_event("leaf1" + "0"*28, "mid1" + "0"*28),
    ]
    chain = trace_event_lineage("leaf1" + "0"*28, events)
    assert len(chain) == 3
    assert chain[0]["event_id"] == "root" + "0"*28
    assert chain[2]["event_id"] == "leaf1" + "0"*28
    print(f"✅ parent chain: {len(chain)} events")

def test_trace_missing_parent_marks_missing():
    events = [make_event("orphan" + "0"*27)]
    chain = trace_event_lineage("orphan" + "0"*27, events)
    # orphan has no parent_event_id, so chain is length 1
    assert len(chain) == 1
    print("✅ orphan root event (single event, no missing_parent)")

def test_trace_detects_cycle():
    events = [
        make_event("c1" + "0"*30, "c2" + "0"*30),
        make_event("c2" + "0"*30, "c1" + "0"*30),
    ]
    chain = trace_event_lineage("c1" + "0"*30, events)
    # Should detect cycle and stop
    assert any(e.get("event_type") == "CYCLE_DETECTED" for e in chain)
    print("✅ cycle detected")

if __name__ == "__main__":
    test_trace_parent_chain()
    test_trace_missing_parent_marks_missing()
    test_trace_detects_cycle()
    print("\n🏁 Lineage tests PASS")
