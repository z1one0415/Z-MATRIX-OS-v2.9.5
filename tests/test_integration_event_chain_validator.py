"""Event Chain Validator tests"""
import sys, os; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from zmatrix.integration.event_chain_validator import (
    build_sample_v3_alpha_event_chain, validate_v3_alpha_event_chain,
)

def test_event_chain_sample_contains_required_event_types():
    c = build_sample_v3_alpha_event_chain()
    types = set(c["event_types"])
    for t in ["PaperLedgerEvent", "OutcomeBackfillEvent", "MemoryCandidateEvent",
              "ApprovalRequestEvent", "HumanApprovalEvent", "PromptPatchEvent", "RiskEvent"]:
        assert t in types
    print("✅ event chain contains all required types")

def test_event_chain_validation_passes():
    c = build_sample_v3_alpha_event_chain()
    r = validate_v3_alpha_event_chain(c)
    assert r["pass"] is True
    print("✅ event chain validation passes")

def test_event_chain_does_not_append():
    c = build_sample_v3_alpha_event_chain()
    assert c["append_allowed"] is False
    print("✅ event chain does not append")

def test_human_approval_event_not_auto_execution():
    c = build_sample_v3_alpha_event_chain()
    r = validate_v3_alpha_event_chain(c)
    has = any("must NOT be interpreted" in v for v in r.get("violations", []))
    assert not has  # no violations
    print("✅ HumanApprovalEvent not auto execution (no violations)")

if __name__ == "__main__":
    test_event_chain_sample_contains_required_event_types()
    test_event_chain_validation_passes()
    test_event_chain_does_not_append()
    test_human_approval_event_not_auto_execution()
    print("\n🏁 Event Chain Validator tests PASS")
