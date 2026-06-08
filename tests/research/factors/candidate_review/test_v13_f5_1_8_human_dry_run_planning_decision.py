"""V13.F5.1.8 — Human dry-run planning decision tests."""
import json, subprocess
from pathlib import Path

D = Path("research/factor_library/reviews/batch_003/f5_1_8_dry_run_planning_decision")

def test_dir_exists(): assert D.exists()

def test_7_files():
    for f in ["batch3_dry_run_planning_decision_record.json","batch3_dry_run_planning_decision_matrix.json","batch3_dry_run_execution_planning_allowed_scope.json","batch3_dry_run_planning_conditions.json","batch3_dry_run_planning_safety_audit.json","batch3_dry_run_planning_decision_closeout.json","batch3_dry_run_planning_next_entry.json"]:
        assert (D / f).exists()

def test_decision():
    r = json.loads((D / "batch3_dry_run_planning_decision_record.json").read_text())
    assert r.get("decision") == "GO_FOR_BATCH3_QUEUE_MONITORING_DRY_RUN_EXECUTION_PLANNING_ONLY"

def test_approved_6():
    r = json.loads((D / "batch3_dry_run_planning_decision_record.json").read_text())
    assert len(r.get("approved_queue",[])) == 6

def test_hold_2():
    r = json.loads((D / "batch3_dry_run_planning_decision_record.json").read_text())
    assert "F26" in r.get("hold_queue",[]) and "F27" in r.get("hold_queue",[])

def test_planning_allowed():
    r = json.loads((D / "batch3_dry_run_planning_decision_record.json").read_text())
    assert r.get("dry_run_execution_planning_allowed") is True

def test_execution_false():
    co = json.loads((D / "batch3_dry_run_planning_decision_closeout.json").read_text())
    for k in ["dry_run_execution_started","monitoring_execution_started","candidate_review_executed","candidate_promotion_executed","factor_calculation_executed","factor_results_modified","runtime_reports_modified","runtime_audit_modified"]:
        assert co.get(k) is False, f"{k} not false"

def test_promotion_alpha_false():
    co = json.loads((D / "batch3_dry_run_planning_decision_closeout.json").read_text())
    for k in ["promotion_allowed","alpha_claim_allowed","multi_factor_composite_built","weight_optimization_executed","paper_trading_started"]:
        assert co.get(k) is False, f"{k} not false"

def test_prod_blocked():
    co = json.loads((D / "batch3_dry_run_planning_decision_closeout.json").read_text())
    for k in ["production","broker_runtime","real_trade"]: assert co.get(k) == "BLOCKED"

def test_f26_auto_unlock_false():
    m = json.loads((D / "batch3_dry_run_planning_decision_matrix.json").read_text())
    f26 = [f for f in m["factors"] if f["factor_id"]=="F26"][0]
    assert f26.get("automatic_unlock_allowed") is False
    assert f26.get("decision") == "HOLD_REMAINS_LOCKED"

def test_f27_auto_unlock_false():
    m = json.loads((D / "batch3_dry_run_planning_decision_matrix.json").read_text())
    f27 = [f for f in m["factors"] if f["factor_id"]=="F27"][0]
    assert f27.get("automatic_unlock_allowed") is False

def test_allowed_scope():
    s = json.loads((D / "batch3_dry_run_execution_planning_allowed_scope.json").read_text())
    assert "dry_run_execution" in s.get("blocked_next_scope",[])
    assert "alpha_claim" in s.get("blocked_next_scope",[])

def test_conditions():
    c = json.loads((D / "batch3_dry_run_planning_conditions.json").read_text())
    assert "dry_run_execution_planning_only" in c.get("approved_factor_conditions",[])
    assert "no_automatic_unlock" in str(c.get("held_factor_conditions",[]))

def test_safety_0():
    s = json.loads((D / "batch3_dry_run_planning_safety_audit.json").read_text())
    assert s.get("violation_count",999) == 0
    for k,v in s.get("checks",{}).items(): assert v is True, f"check: {k}"

def test_next():
    n = json.loads((D / "batch3_dry_run_planning_next_entry.json").read_text())
    assert "V13_F5_1_9" in n.get("next_legal_entry","")

def test_registry():
    reg = json.loads(Path("research/factor_library/registry.json").read_text())
    assert reg.get("dry_run_execution_planning_allowed") is True
    assert reg.get("dry_run_execution_started") is False

def test_skillos(): assert subprocess.run("git diff --name-only -- skillos",shell=True,capture_output=True,text=True).stdout.strip() == ""
def test_runtime(): assert subprocess.run("git diff --name-only -- runtime_reports",shell=True,capture_output=True,text=True).stdout.strip() == ""
def test_audit(): assert subprocess.run("git diff --name-only -- runtime_audit",shell=True,capture_output=True,text=True).stdout.strip() == ""
