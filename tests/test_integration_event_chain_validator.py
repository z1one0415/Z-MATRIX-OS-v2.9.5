"""Event Chain Validator tests"""
import sys, os; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from zmatrix.integration.event_chain_validator import (
    build_sample_v3_alpha_event_chain, validate_v3_alpha_event_chain,
)

def test_event_chain_contains_required_types():
    c = build_sample_v3_alpha_event_chain()
    types = set(c["event_types"])
    for t in ["PaperLedgerEvent","OutcomeBackfillEvent","MemoryCandidateEvent",
              "ApprovalRequestEvent","HumanApprovalEvent","PromptPatchEvent","RiskEvent"]:
        assert t in types
    print("✅ chain contains 7 required event types")

def test_event_chain_validation_passes():
    c = build_sample_v3_alpha_event_chain()
    r = validate_v3_alpha_event_chain(c)
    assert r["pass"] is True, f"violations: {r.get('violations', [])}"
    print("✅ event chain validation passes")

def test_prompt_patch_event_not_runtime_injection():
    c = build_sample_v3_alpha_event_chain()
    prompt = next(e for e in c["events"] if e["event_type"] == "PromptPatchEvent")
    assert prompt["safety"]["prompt_auto_injection_allowed"] is False
    assert prompt["safety"]["system_prompt_write_allowed"] is False
    assert prompt["safety"]["runtime_injection_allowed"] is False
    print("✅ PromptPatchEvent: no injection, no system write")

def test_risk_event_not_real_trade():
    c = build_sample_v3_alpha_event_chain()
    risk = next(e for e in c["events"] if e["event_type"] == "RiskEvent")
    assert risk["safety"]["real_trade_allowed"] is False
    assert risk["safety"]["broker_order_allowed"] is False
    assert risk["safety"]["auto_sell_allowed"] is False
    print("✅ RiskEvent: no trade, no broker, no auto sell")

def test_validator_rejects_prompt_patch_safety_runtime_injection_true():
    c = build_sample_v3_alpha_event_chain()
    prompt = next(e for e in c["events"] if e["event_type"] == "PromptPatchEvent")
    prompt["safety"]["runtime_injection_allowed"] = True
    r = validate_v3_alpha_event_chain(c)
    assert r["pass"] is False
    assert any("PromptPatchEvent must not runtime inject" in v for v in r["violations"])
    print("✅ rejects safety.runtime_injection_allowed=True")

def test_validator_rejects_prompt_patch_safety_system_prompt_write_true():
    c = build_sample_v3_alpha_event_chain()
    prompt = next(e for e in c["events"] if e["event_type"] == "PromptPatchEvent")
    prompt["safety"]["system_prompt_write_allowed"] = True
    r = validate_v3_alpha_event_chain(c)
    assert r["pass"] is False
    assert any("PromptPatchEvent must not write system prompt" in v for v in r["violations"])
    print("✅ rejects safety.system_prompt_write_allowed=True")

def test_validator_rejects_risk_event_auto_sell_true():
    c = build_sample_v3_alpha_event_chain()
    risk = next(e for e in c["events"] if e["event_type"] == "RiskEvent")
    risk["safety"]["auto_sell_allowed"] = True
    r = validate_v3_alpha_event_chain(c)
    assert r["pass"] is False
    assert any("RiskEvent must not auto sell" in v for v in r["violations"])
    print("✅ rejects safety.auto_sell_allowed=True")

def test_validator_rejects_risk_event_auto_position_close_true():
    c = build_sample_v3_alpha_event_chain()
    risk = next(e for e in c["events"] if e["event_type"] == "RiskEvent")
    risk["safety"]["auto_position_close_allowed"] = True
    r = validate_v3_alpha_event_chain(c)
    assert r["pass"] is False
    assert any("RiskEvent must not auto position close" in v for v in r["violations"])
    print("✅ rejects safety.auto_position_close_allowed=True")

if __name__ == "__main__":
    test_event_chain_contains_required_types()
    test_event_chain_validation_passes()
    test_prompt_patch_event_not_runtime_injection()
    test_risk_event_not_real_trade()
    test_validator_rejects_prompt_patch_safety_runtime_injection_true()
    test_validator_rejects_prompt_patch_safety_system_prompt_write_true()
    test_validator_rejects_risk_event_auto_sell_true()
    test_validator_rejects_risk_event_auto_position_close_true()
    print("\n🏁 Event Chain Validator tests PASS")
