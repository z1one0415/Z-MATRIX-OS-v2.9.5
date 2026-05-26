"""Event schema validation tests"""
import sys, os; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from zmatrix.event_store.schemas import EVENT_TYPES, DEFAULT_EVENT_SAFETY
from zmatrix.event_store.validators import validate_event

def test_all_event_types_declared():
    required = {
        "ResearchEvent", "CandidateReviewEvent", "RoleClassificationEvent",
        "PaperDecisionEvent", "PaperLedgerEvent", "OutcomeBackfillEvent",
        "RiskEvent", "HumanDiaryEvent", "MistakeAttributionEvent",
        "MemoryCandidateEvent", "CalibrationEvent", "HumanApprovalEvent",
        "PromptPatchEvent", "ApprovalRequestEvent",
    }
    missing = required - set(EVENT_TYPES)
    assert not missing, f"missing: {missing}"
    print(f"✅ {len(EVENT_TYPES)} EVENT_TYPES declared (all {len(required)} required types present)")

def test_approval_request_event_type_declared():
    assert "ApprovalRequestEvent" in EVENT_TYPES
    assert "HumanApprovalEvent" in EVENT_TYPES
    assert "MemoryCandidateEvent" in EVENT_TYPES
    print("✅ ApprovalRequestEvent, HumanApprovalEvent, MemoryCandidateEvent all declared")

def test_default_safety_blocks_real_ops():
    s = DEFAULT_EVENT_SAFETY
    assert s["real_trade_allowed"] is False
    assert s["real_z9_write_allowed"] is False
    assert s["hermes_memory_write_allowed"] is False
    assert s["prompt_auto_injection_allowed"] is False
    assert s["local_event_write_allowed"] is True
    print("✅ default safety blocks real ops")

def test_validate_event_rejects_real_trade_true():
    event = {
        "event_id": "a"*32, "event_type": "ResearchEvent",
        "schema_version": "EVENT_STORE_V10", "created_at": "now",
        "producer_module": "test", "payload": {},
        "safety": {"real_trade_allowed": True},
    }
    v = validate_event(event)
    assert len(v) > 0
    print(f"✅ real_trade rejected: {v[0]}")

def test_validate_event_rejects_real_z9_write_true():
    event = {
        "event_id": "a"*32, "event_type": "ResearchEvent",
        "schema_version": "EVENT_STORE_V10", "created_at": "now",
        "producer_module": "test", "payload": {},
        "safety": {"real_z9_write_allowed": True},
    }
    v = validate_event(event)
    assert len(v) > 0
    print(f"✅ real_z9_write rejected: {v[0]}")

def test_validate_event_rejects_hermes_memory_write_true():
    event = {
        "event_id": "a"*32, "event_type": "ResearchEvent",
        "schema_version": "EVENT_STORE_V10", "created_at": "now",
        "producer_module": "test", "payload": {},
        "safety": {"hermes_memory_write_allowed": True},
    }
    v = validate_event(event)
    assert len(v) > 0
    print(f"✅ hermes_memory_write rejected: {v[0]}")

def test_validate_event_rejects_prompt_auto_injection_true():
    event = {
        "event_id": "a"*32, "event_type": "ResearchEvent",
        "schema_version": "EVENT_STORE_V10", "created_at": "now",
        "producer_module": "test", "payload": {},
        "safety": {"prompt_auto_injection_allowed": True},
    }
    v = validate_event(event)
    assert len(v) > 0
    print(f"✅ prompt_auto_injection rejected: {v[0]}")

if __name__ == "__main__":
    test_all_event_types_declared()
    test_default_safety_blocks_real_ops()
    test_validate_event_rejects_real_trade_true()
    test_validate_event_rejects_real_z9_write_true()
    test_validate_event_rejects_hermes_memory_write_true()
    test_validate_event_rejects_prompt_auto_injection_true()
    print("\n🏁 Event Schema tests PASS")
