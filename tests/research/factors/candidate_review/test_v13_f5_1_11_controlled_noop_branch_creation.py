"""V13.F5.1.11 clean rebuild — Controlled noop branch creation tests."""
import json
from pathlib import Path
D = Path("research/factor_library/reviews/batch_003/f5_1_11_controlled_noop_branch_creation")

def test_dir(): assert D.exists()
def test_8_files():
    for f in ["batch3_controlled_noop_branch_creation_overview.json","batch3_controlled_noop_branch_gate.json","batch3_controlled_noop_branch_scope.json","batch3_controlled_noop_branch_forbidden_actions.json","batch3_controlled_noop_branch_readiness_checklist.json","batch3_controlled_noop_branch_safety_audit.json","batch3_controlled_noop_branch_decision_record.json","batch3_controlled_noop_branch_closeout.json"]:
        assert (D/f).exists()
def test_base(): c=(D/"batch3_controlled_noop_branch_closeout.json").read_text(); assert "4dd8e86" in c
def test_clean(): co=json.loads((D/"batch3_controlled_noop_branch_closeout.json").read_text()); assert co.get("clean_rebuild") is True
def test_not_created(): co=json.loads((D/"batch3_controlled_noop_branch_closeout.json").read_text()); assert co.get("controlled_noop_dry_run_branch_created") is False
def test_noop_not(): co=json.loads((D/"batch3_controlled_noop_branch_closeout.json").read_text()); assert co.get("noop_runner_implemented") is False
def test_invalidated(): ov=json.loads((D/"batch3_controlled_noop_branch_creation_overview.json").read_text()); assert "0c2e655" in ov.get("invalid_prior_f5_1_10_commit","") and "a6c3ff2" in ov.get("invalid_prior_f5_1_11_commit","")
def test_no_execution():
    co=json.loads((D/"batch3_controlled_noop_branch_closeout.json").read_text())
    for k in ["dry_run_execution_started","monitoring_execution_started","candidate_review_executed","factor_calculation_executed","factor_results_modified","runtime_reports_modified","runtime_audit_modified","external_data_fetch_started"]:
        assert co.get(k) is False
def test_no_promotion(): co=json.loads((D/"batch3_controlled_noop_branch_closeout.json").read_text()); assert co.get("promotion_allowed") is False and co.get("alpha_claim_allowed") is False
def test_prod_blocked(): co=json.loads((D/"batch3_controlled_noop_branch_closeout.json").read_text()); assert co.get("production")=="BLOCKED" and co.get("broker_runtime")=="BLOCKED" and co.get("real_trade")=="BLOCKED"
def test_forbidden_24(): f=json.loads((D/"batch3_controlled_noop_branch_forbidden_actions.json").read_text()); assert f.get("forbidden_count",0)>=24
def test_safety_0(): s=json.loads((D/"batch3_controlled_noop_branch_safety_audit.json").read_text()); assert s.get("violation_count",999)==0
def test_next(): co=json.loads((D/"batch3_controlled_noop_branch_closeout.json").read_text()); assert "CREATE_CLEAN" in co.get("next_legal_entry","")
