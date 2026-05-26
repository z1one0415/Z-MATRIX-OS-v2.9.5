"""Event adapter tests — build only, no auto append"""
import sys, os; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from zmatrix.event_store.adapters import (
    build_paper_ledger_event,
    build_outcome_backfill_event,
    build_role_classification_event,
)

def test_build_paper_ledger_event():
    paper = {"ticker": "002472", "role": "A_LONG_CORE", "action": "BUY",
             "quantity": 300, "price": 45.0}
    ev = build_paper_ledger_event(paper)
    assert ev["event_type"] == "PaperLedgerEvent"
    assert ev["payload"]["ticker"] == "002472"
    assert ev["safety"]["real_trade_allowed"] is False
    print(f"✅ PaperLedgerEvent built: {ev['event_id'][:8]}...")

def test_build_outcome_backfill_event_parent_link():
    outcome = {"ticker": "002472", "status": "COMPLETE", "prediction_id": "p123",
               "result": "+3.2%"}
    parent_id = "a"*32
    ev = build_outcome_backfill_event(outcome, parent_event_id=parent_id)
    assert ev["event_type"] == "OutcomeBackfillEvent"
    assert ev["parent_event_id"] == parent_id
    assert ev["safety"]["hermes_memory_write_allowed"] is False
    print(f"✅ OutcomeBackfillEvent built with parent link")

def test_build_role_classification_event():
    role_result = {"ticker": "002472", "role": "A_LONG_CORE",
                   "b_matrix_score": 7.3, "r_matrix_score": 5.0, "d_matrix_score": 3.0}
    ev = build_role_classification_event(role_result)
    assert ev["event_type"] == "RoleClassificationEvent"
    assert ev["payload"]["role"] == "A_LONG_CORE"
    assert ev["safety"]["real_z9_write_allowed"] is False
    print(f"✅ RoleClassificationEvent built")

def test_adapters_do_not_append_automatically():
    paper = {"ticker": "002472", "role": "A_LONG_CORE", "action": "BUY",
             "quantity": 300, "price": 45.0}
    ev = build_paper_ledger_event(paper)
    # The adapter returns a dict, not a store result
    assert "stored" not in ev
    assert "event_id" in ev
    print("✅ adapter does not auto-append (returns event dict, not store result)")

if __name__ == "__main__":
    test_build_paper_ledger_event()
    test_build_outcome_backfill_event_parent_link()
    test_build_role_classification_event()
    test_adapters_do_not_append_automatically()
    print("\n🏁 Adapter tests PASS")
