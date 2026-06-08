"""V13.F5.1.5 — Batch3 queue monitoring plan tests."""
import json, subprocess
from pathlib import Path

PLAN_DIR = Path("research/factor_library/reviews/batch_003/f5_1_5_queue_monitoring_plan")
REQUIRED = [
    "batch3_queue_monitoring_plan_overview.json",
    "batch3_approved_queue_monitoring_matrix.json",
    "batch3_hold_queue_unlock_monitoring_matrix.json",
    "batch3_monitoring_signal_definition.json",
    "batch3_monitoring_guardrail_matrix.json",
    "batch3_monitoring_evidence_requirements.json",
    "batch3_monitoring_risk_register.json",
    "batch3_monitoring_decision_template.json",
    "batch3_monitoring_safety_audit.json",
    "batch3_monitoring_plan_closeout.json"
]
FORBIDDEN_SIGNALS = ["alpha_signal","buy_signal","sell_signal","order_signal","position_weight_signal","portfolio_signal","broker_signal","real_trade_signal"]

def test_dir_exists():
    assert PLAN_DIR.exists()

def test_10_files():
    for f in REQUIRED: assert (PLAN_DIR / f).exists(), f"Missing: {f}"

def test_approved_6():
    m = json.loads((PLAN_DIR / "batch3_approved_queue_monitoring_matrix.json").read_text())
    assert m.get("factor_count") == 6

def test_hold_2():
    m = json.loads((PLAN_DIR / "batch3_hold_queue_unlock_monitoring_matrix.json").read_text())
    assert m.get("factor_count") == 2

def test_f26_auto_unlock_false():
    m = json.loads((PLAN_DIR / "batch3_hold_queue_unlock_monitoring_matrix.json").read_text())
    f26 = [f for f in m["factors"] if f["factor_id"]=="F26"][0]
    assert f26.get("automatic_unlock_allowed") is False
    assert "HUMAN_HOLD_UNLOCK_DECISION" in f26.get("blocked_until","")

def test_f27_auto_unlock_false():
    m = json.loads((PLAN_DIR / "batch3_hold_queue_unlock_monitoring_matrix.json").read_text())
    f27 = [f for f in m["factors"] if f["factor_id"]=="F27"][0]
    assert f27.get("automatic_unlock_allowed") is False

def test_monitoring_execution_false():
    co = json.loads((PLAN_DIR / "batch3_monitoring_plan_closeout.json").read_text())
    assert co.get("monitoring_execution_started") is False

def test_candidate_review_false():
    co = json.loads((PLAN_DIR / "batch3_monitoring_plan_closeout.json").read_text())
    assert co.get("candidate_review_executed") is False
    assert co.get("candidate_promotion_executed") is False

def test_promotion_alpha_false():
    co = json.loads((PLAN_DIR / "batch3_monitoring_plan_closeout.json").read_text())
    assert co.get("promotion_allowed") is False
    assert co.get("alpha_claim_allowed") is False

def test_composite_weight_false():
    co = json.loads((PLAN_DIR / "batch3_monitoring_plan_closeout.json").read_text())
    assert co.get("multi_factor_composite_built") is False
    assert co.get("weight_optimization_executed") is False

def test_prod_blocked():
    co = json.loads((PLAN_DIR / "batch3_monitoring_plan_closeout.json").read_text())
    assert co.get("production") == "BLOCKED"
    assert co.get("broker_runtime") == "BLOCKED"
    assert co.get("real_trade") == "BLOCKED"

def test_forbidden_signals():
    sd = json.loads((PLAN_DIR / "batch3_monitoring_signal_definition.json").read_text())
    forbidden = sd.get("forbidden_signal_types", [])
    for fs in FORBIDDEN_SIGNALS: assert fs in forbidden, f"Missing forbidden signal: {fs}"

def test_signal_downstream_blocked():
    sd = json.loads((PLAN_DIR / "batch3_monitoring_signal_definition.json").read_text())
    for sig in sd.get("signal_definitions", []):
        assert "Z8_EXECUTION_RUNTIME" in sig.get("blocked_downstream", [])
        assert "BROKER" in sig.get("blocked_downstream", [])
        assert "REAL_TRADE" in sig.get("blocked_downstream", [])
        assert sig.get("alpha_claim_allowed") is False
        assert sig.get("execution_allowed") is False

def test_risk_16():
    r = json.loads((PLAN_DIR / "batch3_monitoring_risk_register.json").read_text())
    assert r.get("risk_count", 0) >= 16

def test_decision_pending():
    d = json.loads((PLAN_DIR / "batch3_monitoring_decision_template.json").read_text())
    assert d.get("decision_status") == "PENDING_HUMAN_REVIEW"

def test_registry_ref():
    reg = json.loads(Path("research/factor_library/registry.json").read_text())
    assert "batch3_queue_monitoring_plan_ref" in reg
    assert reg.get("monitoring_execution_started") is False

def test_safety_0():
    s = json.loads((PLAN_DIR / "batch3_monitoring_safety_audit.json").read_text())
    assert s.get("violation_count", 999) == 0
    for k,v in s.get("checks",{}).items(): assert v is True

def test_next_entry():
    co = json.loads((PLAN_DIR / "batch3_monitoring_plan_closeout.json").read_text())
    assert "HUMAN" in co.get("next_legal_entry", "")

def test_skillos_not_modified():
    r = subprocess.run("git diff --name-only -- skillos", shell=True, capture_output=True, text=True)
    assert r.stdout.strip() == ""

def test_runtime_not_modified():
    r = subprocess.run("git diff --name-only -- runtime_reports", shell=True, capture_output=True, text=True)
    assert r.stdout.strip() == ""
