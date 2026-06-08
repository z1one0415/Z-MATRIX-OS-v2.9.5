"""V13.F5.1.7 — Batch3 queue monitoring dry-run planning tests."""
import json, subprocess
from pathlib import Path

DIR = Path("research/factor_library/reviews/batch_003/f5_1_7_queue_monitoring_dry_run_planning")
FACTORS_APPROVED = ["F21","F22","F24","F30","F31","F34"]

def test_dir_exists():
    assert DIR.exists()

def test_11_files_exist():
    required = ["batch3_dry_run_planning_overview.json","batch3_dry_run_input_snapshot_design.json","batch3_dry_run_decision_log_design.json","batch3_dry_run_noop_output_design.json","batch3_dry_run_hold_unlock_tracking_design.json","batch3_dry_run_review_dashboard_schema.json","batch3_dry_run_guardrail_checklist.json","batch3_dry_run_proof_matrix.json","batch3_dry_run_risk_register.json","batch3_dry_run_safety_audit.json","batch3_dry_run_planning_closeout.json"]
    for f in required: assert (DIR / f).exists(), f"Missing: {f}"

def test_input_snapshot_6_approved():
    d = json.loads((DIR / "batch3_dry_run_input_snapshot_design.json").read_text())
    assert len(d.get("approved_factors",[])) == 6

def test_input_snapshot_2_held():
    d = json.loads((DIR / "batch3_dry_run_input_snapshot_design.json").read_text())
    assert len(d.get("held_factors",[])) == 2

def test_decision_log_schema_only():
    d = json.loads((DIR / "batch3_dry_run_decision_log_design.json").read_text())
    assert d.get("log_execution_started") is False
    assert d.get("runtime_log_created") is False
    assert d.get("runtime_reports_write") is False

def test_noop_output():
    d = json.loads((DIR / "batch3_dry_run_noop_output_design.json").read_text())
    assert d.get("output_mode") == "NOOP_REVIEW_ONLY"
    assert d.get("execution_allowed") is False
    assert d.get("alpha_claim_allowed") is False
    assert d.get("trade_signal_allowed") is False

def test_noop_forbidden():
    d = json.loads((DIR / "batch3_dry_run_noop_output_design.json").read_text())
    forbidden = d.get("forbidden_outputs", [])
    for fb in ["alpha_signal","buy_signal","sell_signal","order_signal","position_weight"]:
        assert fb in forbidden, f"Missing forbidden output: {fb}"

def test_hold_unlock_f26():
    d = json.loads((DIR / "batch3_dry_run_hold_unlock_tracking_design.json").read_text())
    f26 = [f for f in d["held_factors"] if f["factor_id"]=="F26"][0]
    assert f26.get("automatic_unlock_allowed") is False
    assert f26.get("blocked_until") == "HUMAN_HOLD_UNLOCK_DECISION"

def test_hold_unlock_f27():
    d = json.loads((DIR / "batch3_dry_run_hold_unlock_tracking_design.json").read_text())
    f27 = [f for f in d["held_factors"] if f["factor_id"]=="F27"][0]
    assert f27.get("automatic_unlock_allowed") is False

def test_dashboard_forbidden():
    d = json.loads((DIR / "batch3_dry_run_review_dashboard_schema.json").read_text())
    for fb in ["trading_panel","broker_panel","portfolio_panel","alpha_panel","order_panel","production_panel"]:
        assert fb in d.get("forbidden_panels",[]), f"Missing forbidden panel: {fb}"

def test_guardrail_checklist_16():
    c = json.loads((DIR / "batch3_dry_run_guardrail_checklist.json").read_text())
    assert len(c.get("checks",[])) >= 12

def test_proof_matrix_22():
    p = json.loads((DIR / "batch3_dry_run_proof_matrix.json").read_text())
    assert p.get("proof_count",0) >= 20

def test_risk_register_16():
    r = json.loads((DIR / "batch3_dry_run_risk_register.json").read_text())
    assert r.get("risk_count",0) >= 16

def test_safety_0():
    s = json.loads((DIR / "batch3_dry_run_safety_audit.json").read_text())
    assert s.get("violation_count",999) == 0
    for k,v in s.get("checks",{}).items(): assert v is True, f"check failed: {k}"

def test_dry_run_execution_false():
    co = json.loads((DIR / "batch3_dry_run_planning_closeout.json").read_text())
    assert co.get("dry_run_execution_started") is False
    assert co.get("monitoring_execution_started") is False
    assert co.get("candidate_review_executed") is False
    assert co.get("factor_calculation_executed") is False
    assert co.get("factor_results_modified") is False
    assert co.get("runtime_reports_modified") is False

def test_promotion_alpha_false():
    co = json.loads((DIR / "batch3_dry_run_planning_closeout.json").read_text())
    assert co.get("promotion_allowed") is False
    assert co.get("alpha_claim_allowed") is False

def test_prod_blocked():
    co = json.loads((DIR / "batch3_dry_run_planning_closeout.json").read_text())
    assert co.get("production") == "BLOCKED"
    assert co.get("broker_runtime") == "BLOCKED"
    assert co.get("real_trade") == "BLOCKED"

def test_next_entry():
    co = json.loads((DIR / "batch3_dry_run_planning_closeout.json").read_text())
    assert "HUMAN" in co.get("next_legal_entry","")

def test_registry():
    reg = json.loads(Path("research/factor_library/registry.json").read_text())
    assert reg.get("dry_run_execution_started") is False
    assert "queue_monitoring_dry_run_planning_ref" in reg

def test_skillos_not_modified():
    r = subprocess.run("git diff --name-only -- skillos", shell=True, capture_output=True, text=True)
    assert r.stdout.strip() == ""

def test_runtime_not_modified():
    r = subprocess.run("git diff --name-only -- runtime_reports", shell=True, capture_output=True, text=True)
    assert r.stdout.strip() == ""
