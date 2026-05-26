"""Event query and JSONL export/load tests"""
import sys, os; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import tempfile
from zmatrix.event_store.query import filter_events_by_type, filter_events_by_ticker
from zmatrix.event_store.exporters import export_events_to_jsonl, load_events_from_jsonl

def make_event(eid: str, etype: str = "ResearchEvent",
               ticker: str = "002472", producer: str = "test") -> dict:
    return {
        "event_id": eid, "event_type": etype,
        "payload": {"ticker": ticker}, "producer_module": producer,
    }

def test_filter_by_type():
    events = [
        make_event("a"*32, "ResearchEvent"),
        make_event("b"*32, "PaperLedgerEvent"),
        make_event("c"*32, "ResearchEvent"),
    ]
    r = filter_events_by_type(events, "ResearchEvent")
    assert len(r) == 2
    print("✅ filter by type")

def test_filter_by_ticker():
    events = [
        make_event("a"*32, ticker="002472"),
        make_event("b"*32, ticker="601899"),
        make_event("c"*32, ticker="002472"),
    ]
    r = filter_events_by_ticker(events, "002472")
    assert len(r) == 2
    print("✅ filter by ticker")

def test_filter_by_ticker_skips_no_ticker():
    events = [{"event_id": "a"*32, "payload": {}}]
    r = filter_events_by_ticker(events, "002472")
    assert len(r) == 0
    print("✅ filter by ticker skips events without ticker")

def test_export_and_load_jsonl():
    events = [
        make_event("a"*32, "ResearchEvent"),
        make_event("b"*32, "PaperLedgerEvent"),
    ]
    with tempfile.NamedTemporaryFile(suffix=".jsonl", mode="w", delete=False) as f:
        out_path = f.name
    result = export_events_to_jsonl(events, out_path)
    assert result["exported"] == 2
    loaded = load_events_from_jsonl(out_path)
    assert len(loaded) == 2
    os.unlink(out_path)
    print("✅ export/load JSONL round-trip")

if __name__ == "__main__":
    test_filter_by_type()
    test_filter_by_ticker()
    test_filter_by_ticker_skips_no_ticker()
    test_export_and_load_jsonl()
    print("\n🏁 Query & Export tests PASS")
