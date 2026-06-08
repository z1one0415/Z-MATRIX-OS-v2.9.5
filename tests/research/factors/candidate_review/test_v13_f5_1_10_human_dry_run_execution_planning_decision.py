"""V13.F5.1.10 clean rebuild — Dry-run execution planning decision tests."""
import json
from pathlib import Path
D = Path("research/factor_library/reviews/batch_003/f5_1_10_dry_run_execution_planning_decision")

def test_dir(): assert D.exists()
def test_7_files():
    for f in ["batch3_dry_run_execution_planning_decision_record.json","batch3_dry_run_execution_planning_decision_matrix.json","batch3_controlled_noop_dry_run_branch_scope.json","batch3_dry_run_execution_branch_conditions.json","batch3_dry_run_execution_planning_decision_safety_audit.json","batch3_dry_run_execution_planning_decision_closeout.json","batch3_dry_run_execution_planning_next_entry.json"]:
        assert (D/f).exists()
def test_base(): c=(D/"batch3_dry_run_execution_planning_decision_closeout.json").read_text(); assert "4dd8e86" in c
def test_decision(): r=json.loads((D/"batch3_dry_run_execution_planning_decision_record.json").read_text()); assert r.get("decision")=="GO_FOR_CONTROLLED_NOOP_DRY_RUN_EXECUTION_BRANCH_CREATION"
def test_no_execution():
    co=json.loads((D/"batch3_dry_run_execution_planning_decision_closeout.json").read_text())
    for k in ["dry_run_execution_started","monitoring_execution_started","candidate_review_executed","factor_calculation_executed","factor_results_modified","runtime_reports_modified","runtime_audit_modified"]:
        assert co.get(k) is False
def test_no_promotion(): co=json.loads((D/"batch3_dry_run_execution_planning_decision_closeout.json").read_text()); assert co.get("promotion_allowed") is False and co.get("alpha_claim_allowed") is False
def test_prod_blocked(): co=json.loads((D/"batch3_dry_run_execution_planning_decision_closeout.json").read_text()); assert co.get("production")=="BLOCKED" and co.get("broker_runtime")=="BLOCKED" and co.get("real_trade")=="BLOCKED"
def test_approved_6(): r=json.loads((D/"batch3_dry_run_execution_planning_decision_record.json").read_text()); assert len(r.get("approved_queue",[]))==6
def test_hold_2(): r=json.loads((D/"batch3_dry_run_execution_planning_decision_record.json").read_text()); assert len(r.get("hold_queue",[]))==2
def test_safety_0(): s=json.loads((D/"batch3_dry_run_execution_planning_decision_safety_audit.json").read_text()); assert s.get("violation_count",999)==0
