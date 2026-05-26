"""Dry-Run Validator tests"""
import sys, os; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from zmatrix.dry_run.rehearsal_runner import build_v3_alpha_dry_run_rehearsal
from zmatrix.dry_run.rehearsal_validator import validate_v3_alpha_dry_run_rehearsal

def test_dry_run_validation_passes():
    r = build_v3_alpha_dry_run_rehearsal()
    v = validate_v3_alpha_dry_run_rehearsal(r)
    assert v["pass"] is True, f"violations: {v.get('violations', [])}"
    print("✅ dry-run validation passes")

def test_validator_rejects_runtime_enabled_true():
    r = build_v3_alpha_dry_run_rehearsal()
    r["runtime_enabled"] = True
    v = validate_v3_alpha_dry_run_rehearsal(r)
    assert v["pass"] is False
    print("✅ rejects runtime_enabled=True")

def test_validator_rejects_real_trade_true():
    r = build_v3_alpha_dry_run_rehearsal()
    r["real_trade_allowed"] = True
    v = validate_v3_alpha_dry_run_rehearsal(r)
    assert v["pass"] is False
    print("✅ rejects real_trade_allowed=True")

def test_validator_rejects_artifact_safety_real_trade_true():
    r = build_v3_alpha_dry_run_rehearsal()
    r["artifacts"]["paper_ledger_event"]["safety"]["real_trade_allowed"] = True
    v = validate_v3_alpha_dry_run_rehearsal(r)
    assert v["pass"] is False
    assert any("artifacts.paper_ledger_event.safety.real_trade_allowed" in x for x in v["violations"])
    print("✅ rejects artifact safety.real_trade_allowed")

def test_validator_rejects_artifact_safety_hermes_memory_write_true():
    r = build_v3_alpha_dry_run_rehearsal()
    r["artifacts"]["memory_candidate_preview"]["hermes_memory_write_allowed"] = True
    v = validate_v3_alpha_dry_run_rehearsal(r)
    assert v["pass"] is False
    assert any("artifacts.memory_candidate_preview.hermes_memory_write_allowed" in x for x in v["violations"])
    print("✅ rejects artifact hermes_memory_write_allowed")

def test_validator_rejects_prompt_patch_request_safety_auto_injection_true():
    r = build_v3_alpha_dry_run_rehearsal()
    r["artifacts"]["prompt_patch_request"]["safety"]["prompt_auto_injection_allowed"] = True
    v = validate_v3_alpha_dry_run_rehearsal(r)
    assert v["pass"] is False
    assert any("artifacts.prompt_patch_request.safety.prompt_auto_injection_allowed" in x for x in v["violations"])
    print("✅ rejects prompt auto injection")

def test_validator_rejects_prompt_render_runtime_injection_true():
    r = build_v3_alpha_dry_run_rehearsal()
    r["artifacts"]["prompt_render_preview"]["runtime_injection_allowed"] = True
    v = validate_v3_alpha_dry_run_rehearsal(r)
    assert v["pass"] is False
    assert any("artifacts.prompt_render_preview.runtime_injection_allowed" in x for x in v["violations"])
    print("✅ rejects render runtime injection")

def test_validator_rejects_tail_risk_safety_auto_sell_true():
    r = build_v3_alpha_dry_run_rehearsal()
    r["artifacts"]["tail_risk_controller_preview"]["safety"]["auto_sell_allowed"] = True
    v = validate_v3_alpha_dry_run_rehearsal(r)
    assert v["pass"] is False
    assert any("artifacts.tail_risk_controller_preview.safety.auto_sell_allowed" in x for x in v["violations"])
    print("✅ rejects tail risk auto sell")

def test_validator_rejects_non_dict_artifact_safety():
    r = build_v3_alpha_dry_run_rehearsal()
    r["artifacts"]["paper_ledger_event"]["safety"] = "bad"
    v = validate_v3_alpha_dry_run_rehearsal(r)
    assert v["pass"] is False
    assert any("artifacts.paper_ledger_event.safety must be dict" in x for x in v["violations"])
    print("✅ rejects non-dict artifact safety")

if __name__ == "__main__":
    test_dry_run_validation_passes()
    test_validator_rejects_runtime_enabled_true()
    test_validator_rejects_real_trade_true()
    test_validator_rejects_artifact_safety_real_trade_true()
    test_validator_rejects_artifact_safety_hermes_memory_write_true()
    test_validator_rejects_prompt_patch_request_safety_auto_injection_true()
    test_validator_rejects_prompt_render_runtime_injection_true()
    test_validator_rejects_tail_risk_safety_auto_sell_true()
    test_validator_rejects_non_dict_artifact_safety()
    print("\n🏁 Dry-Run Validator tests PASS")
