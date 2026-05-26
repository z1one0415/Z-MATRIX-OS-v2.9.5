"""Event ID generation tests"""
import sys, os; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from zmatrix.event_store.event_ids import build_event_id, hash_payload

def test_event_id_is_32_hex():
    eid = build_event_id("ResearchEvent", {"ticker":"002472"}, "2026-05-26T13:00:00Z")
    assert len(eid) == 32
    assert all(c in "0123456789abcdef" for c in eid)
    print(f"✅ event_id is 32-char hex: {eid}")

def test_hash_payload_is_stable():
    h1 = hash_payload({"ticker":"002472", "score": 75})
    h2 = hash_payload({"score": 75, "ticker":"002472"})
    assert h1 == h2
    assert len(h1) == 64
    print(f"✅ hash_payload stable: {h1[:16]}...")

def test_event_id_stable_for_same_payload():
    e1 = build_event_id("ResearchEvent", {"ticker":"002472"}, "2026-05-26T13:00:00Z")
    e2 = build_event_id("ResearchEvent", {"ticker":"002472"}, "2026-05-26T13:00:00Z")
    assert e1 == e2
    print(f"✅ event_id stable: {e1}")

def test_event_id_differs_for_different_type():
    e1 = build_event_id("ResearchEvent", {"ticker":"002472"}, "2026-05-26T13:00:00Z")
    e2 = build_event_id("PaperLedgerEvent", {"ticker":"002472"}, "2026-05-26T13:00:00Z")
    assert e1 != e2
    print("✅ event_id differs for different type")

if __name__ == "__main__":
    test_event_id_is_32_hex()
    test_hash_payload_is_stable()
    test_event_id_stable_for_same_payload()
    test_event_id_differs_for_different_type()
    print("\n🏁 Event ID tests PASS")
