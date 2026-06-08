"""V13.F5.1.6 — Human queue monitoring plan decision tests."""
import json, subprocess
from pathlib import Path

DECISION_DIR = Path("research/factor_library/reviews/batch_003/f5_1_6_queue_monitoring_plan_decision")

def test_dir_exists():
    assert DECISION_DIR.exists()

def test_7_files():
    required = ["batch3_queue_monitoring_plan_decision_record.json","batch3_queue_monitoring_plan_decision_matrix.json","batch3_queue_monitoring_plan_approved_scope.json","batch3_queue_monitoring_plan_conditions.json","batch3_queue_monitoring_plan_safety_audit.json","batch3_queue_monitoring_plan_decision_closeout.json","batch3_queue_monitoring_plan_next_entry.json"]
    for f in required: assert (DECISION_DIR / f).exists(), f"Missing: {f}"

def test_decision():
    r = json.loads((DECISION_DIR / "batch3_queue_monitoring_plan_decision_record.json").read_text())
    assert r.get("decision") == "GO_FOR_BATCH3_QUEUE_MONITORING_DRY_RUN_PLANNING_ONLY"

def test_approved_6():
    r = json.loads((DECISION_DIR / "batch3_queue_monitoring_plan_decision_record.json").read_text())
    assert len(r.get("approved_queue",[])) == 6

def test_hold_2():
    r = json.loads((DECISION_DIR / "batch3_queue_monitoring_plan_decision_record.json").read_text())
    assert "F26" in r.get("hold_queue",[])
    assert "F27" in r.get("hold_queue",[])

def test_rejected_empty():
    r = json.loads((DECISION_DIR / "batch3_queue_monitoring_plan_decision_record.json").read_text())
    assert r.get("rejected_queue") == []

def test_dry_run_true():
    co = json.loads((DECISION_DIR / "batch3_queue_monitoring_plan_decision_closeout.json").read_text())
    assert co.get("monitoring_dry_run_planning_allowed") is True

def test_monitoring_execution_false():
    co = json.loads((DECISION_DIR / "batch3_queue_monitoring_plan_decision_closeout.json").read_text())
    assert co.get("monitoring_execution_started") is False

def test_candidate_review_false():
    co = json.loads((DECISION_DIR / "batch3_queue_monitoring_plan_decision_closeout.json").read_text())
    assert co.get("candidate_review_executed") is False
    assert co.get("candidate_promotion_executed") is False

def test_promotion_alpha_false():
    co = json.loads((DECISION_DIR / "batch3_queue_monitoring_plan_decision_closeout.json").read_text())
    assert co.get("promotion_allowed") is False
    assert co.get("alpha_claim_allowed") is False

def test_composite_weight_false():
    co = json.loads((DECISION_DIR / "batch3_queue_monitoring_plan_decision_closeout.json").read_text())
    assert co.get("multi_factor_composite_built") is False
    assert co.get("weight_optimization_executed") is False

def test_prod_blocked():
    co = json.loads((DECISION_DIR / "batch3_queue_monitoring_plan_decision_closeout.json").read_text())
    assert co.get("production") == "BLOCKED"
    assert co.get("broker_runtime") == "BLOCKED"
    assert co.get("real_trade") == "BLOCKED"

def test_f26_no_auto():
    m = json.loads((DECISION_DIR / "batch3_queue_monitoring_plan_decision_matrix.json").read_text())
    f26 = [f for f in m["factors"] if f["factor_id"]=="F26"][0]
    assert f26.get("automatic_unlock_allowed") is False
    assert f26.get("decision") == "HOLD_REMAINS_LOCKED"

def test_f27_no_auto():
    m = json.loads((DECISION_DIR / "batch3_queue_monitoring_plan_decision_matrix.json").read_text())
    f27 = [f for f in m["factors"] if f["factor_id"]=="F27"][0]
    assert f27.get("automatic_unlock_allowed") is False
    assert f27.get("decision") == "HOLD_REMAINS_LOCKED"

def test_approved_scope():
    s = json.loads((DECISION_DIR / "batch3_queue_monitoring_plan_approved_scope.json").read_text())
    assert "monitoring_execution" in s.get("blocked_next_scope",[])
    assert "candidate_review_execution" in s.get("blocked_next_scope",[])
    assert "alpha_claim" in s.get("blocked_next_scope",[])

def test_conditions():
    c = json.loads((DECISION_DIR / "batch3_queue_monitoring_plan_conditions.json").read_text())
    assert "no_monitoring_execution" in c.get("approved_factor_conditions",[])
    assert "no_automatic_unlock" in str(c.get("held_factor_conditions",[]))

def test_safety_0():
    s = json.loads((DECISION_DIR / "batch3_queue_monitoring_plan_safety_audit.json").read_text())
    assert s.get("violation_count", 999) == 0
    for k,v in s.get("checks",{}).items(): assert v is True, f"check failed: {k}"

def test_next_entry():
    n = json.loads((DECISION_DIR / "batch3_queue_monitoring_plan_next_entry.json").read_text())
    assert "V13_F5_1_7" in n.get("next_legal_entry","")

def test_registry():
    reg = json.loads(Path("research/factor_library/registry.json").read_text())
    assert reg.get("monitoring_dry_run_planning_allowed") is True
    assert reg.get("monitoring_execution_started") is False
    assert "queue_monitoring_plan_decision_ref" in reg

def test_skillos_not_modified():
    r = subprocess.run("git diff --name-only -- skillos", shell=True, capture_output=True, text=True)
    assert r.stdout.strip() == ""

def test_runtime_not_modified():
    r = subprocess.run("git diff --name-only -- runtime_reports", shell=True, capture_output=True, text=True)
    assert r.stdout.strip() == ""
