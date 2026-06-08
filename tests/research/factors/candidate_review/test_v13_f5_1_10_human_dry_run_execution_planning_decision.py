"""V13.F5.1.10 — Human dry-run execution planning decision tests."""
import json, subprocess
from pathlib import Path

D = Path("research/factor_library/reviews/batch_003/f5_1_10_dry_run_execution_planning_decision")

def test_dir(): assert D.exists()

def test_7_files():
    for f in ["batch3_dry_run_execution_planning_decision_record.json","batch3_dry_run_execution_planning_decision_matrix.json","batch3_controlled_noop_dry_run_branch_scope.json","batch3_dry_run_execution_branch_conditions.json","batch3_dry_run_execution_planning_decision_safety_audit.json","batch3_dry_run_execution_planning_decision_closeout.json","batch3_dry_run_execution_planning_next_entry.json"]:
        assert (D/f).exists(), f"Missing: {f}"

def test_decision():
    r = json.loads((D/"batch3_dry_run_execution_planning_decision_record.json").read_text())
    assert r.get("decision") == "GO_FOR_CONTROLLED_NOOP_DRY_RUN_EXECUTION_BRANCH_CREATION"

def test_approved_6():
    r = json.loads((D/"batch3_dry_run_execution_planning_decision_record.json").read_text())
    assert len(r.get("approved_queue",[])) == 6

def test_hold_2():
    r = json.loads((D/"batch3_dry_run_execution_planning_decision_record.json").read_text())
    assert "F26" in r.get("hold_queue",[]) and "F27" in r.get("hold_queue",[])

def test_branch_allowed():
    r = json.loads((D/"batch3_dry_run_execution_planning_decision_record.json").read_text())
    assert r.get("controlled_noop_dry_run_branch_allowed") is True

def test_execution_false():
    co = json.loads((D/"batch3_dry_run_execution_planning_decision_closeout.json").read_text())
    for k in ["dry_run_execution_started","monitoring_execution_started","candidate_review_executed","candidate_promotion_executed","factor_calculation_executed","factor_results_modified","runtime_reports_modified","runtime_audit_modified","external_data_fetch_started"]:
        assert co.get(k) is False, f"{k} not false"

def test_promotion_alpha():
    co = json.loads((D/"batch3_dry_run_execution_planning_decision_closeout.json").read_text())
    for k in ["promotion_allowed","alpha_claim_allowed","multi_factor_composite_built","weight_optimization_executed","paper_trading_started"]:
        assert co.get(k) is False, f"{k} not false"

def test_prod():
    co = json.loads((D/"batch3_dry_run_execution_planning_decision_closeout.json").read_text())
    for k in ["production","broker_runtime","real_trade"]: assert co.get(k)=="BLOCKED", f"{k} not BLOCKED"

def test_f26_no_auto():
    m = json.loads((D/"batch3_dry_run_execution_planning_decision_matrix.json").read_text())
    f26 = [f for f in m["factors"] if f["factor_id"]=="F26"][0]
    assert f26.get("automatic_unlock_allowed") is False
    assert f26.get("decision") == "HOLD_REMAINS_LOCKED"

def test_f27_no_auto():
    m = json.loads((D/"batch3_dry_run_execution_planning_decision_matrix.json").read_text())
    f27 = [f for f in m["factors"] if f["factor_id"]=="F27"][0]
    assert f27.get("automatic_unlock_allowed") is False

def test_allowed_scope():
    s = json.loads((D/"batch3_controlled_noop_dry_run_branch_scope.json").read_text())
    assert "real_dry_run_execution" in s.get("blocked_next_scope",[])
    assert "alpha_claim" in s.get("blocked_next_scope",[])
    assert "create_controlled_noop_dry_run_branch" in s.get("allowed_next_scope",[])

def test_conditions():
    c = json.loads((D/"batch3_dry_run_execution_branch_conditions.json").read_text())
    assert "noop_runner_only" in c.get("approved_factor_conditions",[])
    assert "no_automatic_unlock" in str(c.get("held_factor_conditions",[]))

def test_safety_0():
    s = json.loads((D/"batch3_dry_run_execution_planning_decision_safety_audit.json").read_text())
    assert s.get("violation_count",999) == 0
    for v in s.get("checks",{}).values(): assert v is True

def test_next():
    co = json.loads((D/"batch3_dry_run_execution_planning_decision_closeout.json").read_text())
    n = json.loads((D/"batch3_dry_run_execution_planning_next_entry.json").read_text())
    assert "CREATE_CONTROLLED_NOOP_DRY_RUN_EXECUTION_BRANCH_ONLY" in co.get("next_legal_entry","")
    assert "CREATE_CONTROLLED_NOOP_DRY_RUN_EXECUTION_BRANCH_ONLY" in n.get("next_legal_entry","")

def test_registry():
    reg = json.loads(Path("research/factor_library/registry.json").read_text())
    assert reg.get("controlled_noop_dry_run_branch_allowed") is True
    assert reg.get("dry_run_execution_started") is False

def test_skillos(): assert subprocess.run("git diff --name-only -- skillos",shell=True,capture_output=True,text=True).stdout.strip() == ""
def test_runtime(): assert subprocess.run("git diff --name-only -- runtime_reports",shell=True,capture_output=True,text=True).stdout.strip() == ""
def test_audit(): assert subprocess.run("git diff --name-only -- runtime_audit",shell=True,capture_output=True,text=True).stdout.strip() == ""
