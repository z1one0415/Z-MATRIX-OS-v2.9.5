"""V13.F5.1.9 — Dry-run execution planning tests."""
import json, subprocess
from pathlib import Path

D = Path("research/factor_library/reviews/batch_003/f5_1_9_dry_run_execution_planning")
F12 = ["batch3_dry_run_execution_planning_overview.json","batch3_dry_run_execution_input_freeze_plan.json","batch3_dry_run_noop_runner_contract.json","batch3_dry_run_decision_log_contract.json","batch3_dry_run_noop_output_artifact_plan.json","batch3_dry_run_safety_guard_plan.json","batch3_dry_run_hold_unlock_noop_plan.json","batch3_dry_run_rollback_plan.json","batch3_dry_run_execution_proof_matrix.json","batch3_dry_run_execution_risk_register.json","batch3_dry_run_execution_safety_audit.json","batch3_dry_run_execution_planning_closeout.json"]

def test_dir(): assert D.exists()

def test_12_files():
    for f in F12: assert (D / f).exists(), f"Missing: {f}"

def test_approved_6():
    d = json.loads((D / "batch3_dry_run_execution_input_freeze_plan.json").read_text())
    assert len(d.get("approved_factors",[])) == 6

def test_held_2():
    d = json.loads((D / "batch3_dry_run_execution_input_freeze_plan.json").read_text())
    assert len(d.get("held_factors",[])) == 2

def test_noop_runner():
    r = json.loads((D / "batch3_dry_run_noop_runner_contract.json").read_text())
    assert r.get("runner_execution_started") is False
    assert r.get("runner_execution_allowed_now") is False
    assert r.get("side_effects_allowed") is False

def test_decision_log():
    d = json.loads((D / "batch3_dry_run_decision_log_contract.json").read_text())
    assert d.get("decision_log_created_now") is False
    assert d.get("runtime_log_created") is False
    assert d.get("runtime_reports_write") is False
    assert d.get("runtime_audit_write") is False

def test_noop_artifact():
    a = json.loads((D / "batch3_dry_run_noop_output_artifact_plan.json").read_text())
    assert a.get("artifact_creation_now") is False
    assert a.get("execution_allowed") is False

def test_forbidden_artifacts():
    a = json.loads((D / "batch3_dry_run_noop_output_artifact_plan.json").read_text())
    fb = a.get("forbidden_artifacts",[])
    for item in ["alpha_signal","buy_signal","sell_signal","order_signal","position_weight","broker_payload","real_trade_payload"]:
        assert item in fb, f"Missing forbidden: {item}"

def test_safety_guards():
    g = json.loads((D / "batch3_dry_run_safety_guard_plan.json").read_text())
    assert g.get("guard_count",0) >= 18

def test_safety_guard_action():
    g = json.loads((D / "batch3_dry_run_safety_guard_plan.json").read_text())
    for gd in g.get("guards",[]):
        assert gd.get("action") == "KILL_AND_NOOP"

def test_hold_unlock():
    h = json.loads((D / "batch3_dry_run_hold_unlock_noop_plan.json").read_text())
    f26 = [f for f in h["held_factors"] if f["factor_id"]=="F26"][0]
    assert f26.get("automatic_unlock_allowed") is False
    assert f26.get("dry_run_can_only_report_blocked_status") is True

def test_f27_no_auto():
    h = json.loads((D / "batch3_dry_run_hold_unlock_noop_plan.json").read_text())
    f27 = [f for f in h["held_factors"] if f["factor_id"]=="F27"][0]
    assert f27.get("automatic_unlock_allowed") is False

def test_rollback():
    r = json.loads((D / "batch3_dry_run_rollback_plan.json").read_text())
    assert len(r.get("rollback_actions",[])) >= 8

def test_proof():
    p = json.loads((D / "batch3_dry_run_execution_proof_matrix.json").read_text())
    assert p.get("proof_count",0) >= 24

def test_risk():
    r = json.loads((D / "batch3_dry_run_execution_risk_register.json").read_text())
    assert r.get("risk_count",0) >= 16

def test_safety_0():
    s = json.loads((D / "batch3_dry_run_execution_safety_audit.json").read_text())
    assert s.get("violation_count",999) == 0
    for v in s.get("checks",{}).values():
        assert v is True

def test_closeout_execution_false():
    co = json.loads((D / "batch3_dry_run_execution_planning_closeout.json").read_text())
    for k in ["dry_run_execution_started","monitoring_execution_started","candidate_review_executed","factor_calculation_executed","factor_results_modified","runtime_reports_modified","runtime_audit_modified","external_data_fetch_started"]:
        assert co.get(k) is False, f"{k} not false"

def test_promotion_alpha():
    co = json.loads((D / "batch3_dry_run_execution_planning_closeout.json").read_text())
    assert co.get("promotion_allowed") is False
    assert co.get("alpha_claim_allowed") is False

def test_prod():
    co = json.loads((D / "batch3_dry_run_execution_planning_closeout.json").read_text())
    for k in ["production","broker_runtime","real_trade"]:
        assert co.get(k) == "BLOCKED", f"{k} not BLOCKED"

def test_next():
    co = json.loads((D / "batch3_dry_run_execution_planning_closeout.json").read_text())
    assert "HUMAN" in co.get("next_legal_entry","")

def test_registry():
    reg = json.loads(Path("research/factor_library/registry.json").read_text())
    assert reg.get("dry_run_execution_started") is False
    assert "dry_run_execution_planning_ref" in reg

def test_skillos():
    r = subprocess.run("git diff --name-only -- skillos",shell=True,capture_output=True,text=True)
    assert r.stdout.strip() == ""

def test_runtime():
    r = subprocess.run("git diff --name-only -- runtime_reports",shell=True,capture_output=True,text=True)
    assert r.stdout.strip() == ""

def test_audit():
    r = subprocess.run("git diff --name-only -- runtime_audit",shell=True,capture_output=True,text=True)
    assert r.stdout.strip() == ""
