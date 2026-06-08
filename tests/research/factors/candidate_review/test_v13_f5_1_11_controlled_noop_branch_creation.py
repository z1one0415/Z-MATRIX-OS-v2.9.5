"""V13.F5.1.11 — Controlled noop branch creation tests."""
import json, subprocess
from pathlib import Path
D = Path("research/factor_library/reviews/batch_003/f5_1_11_controlled_noop_branch_creation")

def test_dir():
    assert D.exists()

def test_8_files():
    names = ["batch3_controlled_noop_branch_creation_overview.json","batch3_controlled_noop_branch_gate.json","batch3_controlled_noop_branch_scope.json","batch3_controlled_noop_branch_forbidden_actions.json","batch3_controlled_noop_branch_readiness_checklist.json","batch3_controlled_noop_branch_safety_audit.json","batch3_controlled_noop_branch_decision_record.json","batch3_controlled_noop_branch_closeout.json"]
    for f in names:
        assert (D / f).exists()

def test_status():
    co = json.loads((D / "batch3_controlled_noop_branch_closeout.json").read_text())
    assert co.get("status") == "V13_F5_1_11_CONTROLLED_NOOP_DRY_RUN_BRANCH_CREATED"
    assert co.get("noop_runner_implemented") is False

def test_execution_false():
    co = json.loads((D / "batch3_controlled_noop_branch_closeout.json").read_text())
    keys = ["dry_run_execution_started","monitoring_execution_started","candidate_review_executed","factor_calculation_executed","factor_results_modified","runtime_reports_modified","runtime_audit_modified","external_data_fetch_started"]
    for k in keys:
        assert co.get(k) is False

def test_promotion_alpha():
    co = json.loads((D / "batch3_controlled_noop_branch_closeout.json").read_text())
    assert co.get("promotion_allowed") is False
    assert co.get("alpha_claim_allowed") is False

def test_prod_blocked():
    co = json.loads((D / "batch3_controlled_noop_branch_closeout.json").read_text())
    assert co.get("production") == "BLOCKED"
    assert co.get("broker_runtime") == "BLOCKED"
    assert co.get("real_trade") == "BLOCKED"

def test_forbidden_24():
    f = json.loads((D / "batch3_controlled_noop_branch_forbidden_actions.json").read_text())
    assert f.get("forbidden_count") >= 24

def test_readiness_20():
    ch = json.loads((D / "batch3_controlled_noop_branch_readiness_checklist.json").read_text())
    assert ch.get("checklist_count") >= 20

def test_safety_0():
    s = json.loads((D / "batch3_controlled_noop_branch_safety_audit.json").read_text())
    assert s.get("violation_count", 999) == 0

def test_next():
    co = json.loads((D / "batch3_controlled_noop_branch_closeout.json").read_text())
    assert "P0_IMPLEMENTATION_PLANNING_ONLY" in co.get("next_legal_entry", "")

def test_gate():
    g = json.loads((D / "batch3_controlled_noop_branch_gate.json").read_text())
    assert g.get("implementation_allowed_now") is False

def test_branch_exists():
    r = subprocess.run("git branch --list impl/research-batch3-controlled-noop-dry-run-execution-p0", shell=True, capture_output=True, text=True)
    assert "impl/research-batch3-controlled-noop-dry-run-execution-p0" in r.stdout
