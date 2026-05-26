"""Local EventStore SQLite tests — append, idempotent, conflict"""
import sys, os; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import tempfile
from zmatrix.event_store.store import LocalEventStore

def _make_event(event_id: str, event_type: str = "ResearchEvent",
                payload: dict | None = None) -> dict:
    return {
        "event_id": event_id, "event_type": event_type,
        "schema_version": "EVENT_STORE_V10", "created_at": "2026-05-26T13:00:00Z",
        "producer_module": "test", "source_event_id": None,
        "parent_event_id": None, "input_hash": "a"*64, "output_hash": "b"*64,
        "payload": payload or {"ticker": "002472"},
        "safety": {
            "real_trade_allowed": False, "broker_order_allowed": False,
            "real_z9_write_allowed": False, "hermes_memory_write_allowed": False,
            "auto_calibration_allowed": False, "prompt_auto_injection_allowed": False,
            "local_event_write_allowed": True,
        },
    }

def test_initialize_sqlite_store():
    with tempfile.NamedTemporaryFile(suffix=".sqlite", delete=False) as f:
        db_path = f.name
    store = LocalEventStore(db_path)
    store.initialize()
    store.close()
    assert os.path.exists(db_path)
    os.unlink(db_path)
    print("✅ SQLite store initialized")

def test_append_event_success():
    with tempfile.NamedTemporaryFile(suffix=".sqlite", delete=False) as f:
        db_path = f.name
    store = LocalEventStore(db_path)
    store.initialize()
    ev = _make_event("a"*32)
    r = store.append_event(ev)
    assert r["stored"] is True
    assert r["idempotent"] is False
    assert r["conflict"] is False
    store.close()
    os.unlink(db_path)
    print("✅ append event success")

def test_append_event_idempotent_same_payload():
    with tempfile.NamedTemporaryFile(suffix=".sqlite", delete=False) as f:
        db_path = f.name
    store = LocalEventStore(db_path)
    store.initialize()
    ev = _make_event("b"*32)
    r1 = store.append_event(ev)
    assert r1["stored"] is True
    r2 = store.append_event(ev)
    assert r2["idempotent"] is True
    assert r2["stored"] is True
    store.close()
    os.unlink(db_path)
    print("✅ idempotent same payload")

def test_append_event_conflict_different_payload():
    with tempfile.NamedTemporaryFile(suffix=".sqlite", delete=False) as f:
        db_path = f.name
    store = LocalEventStore(db_path)
    store.initialize()
    ev1 = _make_event("c"*32, payload={"ticker": "002472"})
    ev2 = _make_event("c"*32, payload={"ticker": "601899"})
    r1 = store.append_event(ev1)
    assert r1["stored"] is True
    r2 = store.append_event(ev2)
    assert r2["stored"] is False
    assert r2["conflict"] is True
    store.close()
    os.unlink(db_path)
    print("✅ conflict detection")

def test_list_events_by_type():
    with tempfile.NamedTemporaryFile(suffix=".sqlite", delete=False) as f:
        db_path = f.name
    store = LocalEventStore(db_path)
    store.initialize()
    store.append_event(_make_event("d1"+"0"*30, event_type="ResearchEvent"))
    store.append_event(_make_event("e1"+"0"*30, event_type="PaperLedgerEvent"))
    all_events = store.list_events()
    assert len(all_events) == 2
    filtered = store.list_events(event_type="ResearchEvent")
    assert len(filtered) == 1
    store.close()
    os.unlink(db_path)
    print("✅ list events by type")

def test_no_real_z9_write_on_append():
    with tempfile.NamedTemporaryFile(suffix=".sqlite", delete=False) as f:
        db_path = f.name
    store = LocalEventStore(db_path)
    store.initialize()
    ev = _make_event("f"*32)
    r = store.append_event(ev)
    assert r["real_z9_write_allowed"] is False
    store.close()
    os.unlink(db_path)
    print("✅ no real Z9 write on append")

def test_no_hermes_memory_write_on_append():
    with tempfile.NamedTemporaryFile(suffix=".sqlite", delete=False) as f:
        db_path = f.name
    store = LocalEventStore(db_path)
    store.initialize()
    ev = _make_event("g"*32)
    r = store.append_event(ev)
    assert r["hermes_memory_write_allowed"] is False
    store.close()
    os.unlink(db_path)
    print("✅ no Hermes memory write on append")

if __name__ == "__main__":
    test_initialize_sqlite_store()
    test_append_event_success()
    test_append_event_idempotent_same_payload()
    test_append_event_conflict_different_payload()
    test_list_events_by_type()
    test_no_real_z9_write_on_append()
    test_no_hermes_memory_write_on_append()
    print("\n🏁 Local EventStore tests PASS")
