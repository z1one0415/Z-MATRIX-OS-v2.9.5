"""Event adapter tests — build only, no auto append"""
import sys, os; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from zmatrix.event_store.adapters import (
    build_paper_ledger_event,
    build_outcome_backfill_event,
    build_role_classification_event,
)

def test_build_paper_ledger_event():
    paper = {"ticker": "002472", "role": "A_LONG_CORE", "paper_action": "BUY",
             "entry_price": 45.0}
    ev = build_paper_ledger_event(paper)
    assert ev["event_type"] == "PaperLedgerEvent"
    assert ev["payload"]["ticker"] == "002472"
    assert ev["safety"]["real_trade_allowed"] is False
    print(f"✅ PaperLedgerEvent built: {ev['event_id'][:8]}...")

def test_build_outcome_backfill_event_parent_link():
    outcome = {"ticker": "002472", "outcome_status": "COMPLETE",
               "actual_return_t5": 3.2}
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
    paper = {"ticker": "002472", "role": "A_LONG_CORE", "paper_action": "BUY"}
    ev = build_paper_ledger_event(paper)
    assert "stored" not in ev
    assert "event_id" in ev
    print("✅ adapter does not auto-append (returns event dict, not store result)")

def test_paper_ledger_event_preserves_v299_fields():
    paper = {
        "paper_id": "p1",
        "ticker": "002472",
        "role": "B_MID_ROTATION",
        "entry_date": "2026-01-01",
        "entry_price": 10.5,
        "paper_action": "PAPER_TRACK",
        "target_horizon": "T20",
        "max_loss_plan": 0.01,
        "invalidation_condition": "break thesis",
    }
    ev = build_paper_ledger_event(paper)
    payload = ev["payload"]
    assert payload["paper_id"] == "p1"
    assert payload["entry_price"] == 10.5
    assert payload["paper_action"] == "PAPER_TRACK"
    assert payload["target_horizon"] == "T20"
    assert "stored" not in ev
    print("✅ paper adapter preserves v2.9.9 fields (paper_id, entry_price, paper_action, target_horizon)")

def test_outcome_event_preserves_v299_fields():
    outcome = {
        "paper_id": "p1",
        "ticker": "002472",
        "entry_date": "2026-01-01",
        "actual_return_t5": 1.0,
        "actual_return_t20": 3.5,
        "actual_return_t60": None,
        "max_drawdown_t20": 2.0,
        "max_drawdown_t60": None,
        "outcome_status": "READY",
        "error_type": "",
        "review_note": "ok",
    }
    ev = build_outcome_backfill_event(outcome)
    payload = ev["payload"]
    assert payload["paper_id"] == "p1"
    assert payload["actual_return_t20"] == 3.5
    assert payload["outcome_status"] == "READY"
    assert "stored" not in ev
    print("✅ outcome adapter preserves v2.9.9 fields (actual_return_t*, max_drawdown, outcome_status)")

if __name__ == "__main__":
    test_build_paper_ledger_event()
    test_build_outcome_backfill_event_parent_link()
    test_build_role_classification_event()
    test_adapters_do_not_append_automatically()
    test_paper_ledger_event_preserves_v299_fields()
    test_outcome_event_preserves_v299_fields()
    print("\n🏁 Adapter tests PASS")
