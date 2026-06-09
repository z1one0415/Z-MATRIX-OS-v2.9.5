"""
V13.F5.1.14 Human Controlled Noop P0 Implementation Planning Decision Tests.

Verifies:
- Decision directory and 7 files exist
- Decision = GO_FOR_CONTROLLED_NOOP_DRY_RUN_P0_IMPLEMENTATION_BRANCH
- All safety invariants maintained
- No implementation, no execution, no side effects
- Next entry = CREATE_CONTROLLED_NOOP_DRY_RUN_P0_IMPLEMENTATION_BRANCH_ONLY
"""

import json
from pathlib import Path

DECISION_DIR = Path(
    "research/factor_library/reviews/batch_003/f5_1_14_p0_implementation_planning_decision"
)

EXPECTED_FILES = [
    "batch3_p0_implementation_planning_decision_record.json",
    "batch3_p0_implementation_planning_decision_matrix.json",
    "batch3_p0_implementation_branch_scope.json",
    "batch3_p0_implementation_branch_conditions.json",
    "batch3_p0_implementation_planning_decision_safety_audit.json",
    "batch3_p0_implementation_planning_decision_closeout.json",
    "batch3_p0_implementation_planning_next_entry.json",
]


def _load(name: str) -> dict:
    return json.loads((DECISION_DIR / name).read_text())


# 1. Decision directory exists
def test_decision_directory_exists():
    assert DECISION_DIR.exists()
    assert DECISION_DIR.is_dir()


# 2. All 7 decision files exist
def test_7_decision_files_exist():
    for name in EXPECTED_FILES:
        assert (DECISION_DIR / name).exists(), f"Missing: {name}"


# 3. Decision = GO_FOR_CONTROLLED_NOOP_DRY_RUN_P0_IMPLEMENTATION_BRANCH
def test_decision_go():
    rec = _load("batch3_p0_implementation_planning_decision_record.json")
    assert rec["decision"] == "GO_FOR_CONTROLLED_NOOP_DRY_RUN_P0_IMPLEMENTATION_BRANCH"


# 4. implementation_branch_allowed true
def test_implementation_branch_allowed():
    rec = _load("batch3_p0_implementation_planning_decision_record.json")
    assert rec["implementation_branch_allowed"] is True


# 5. noop_runner_implemented false
def test_noop_runner_not_implemented():
    rec = _load("batch3_p0_implementation_planning_decision_record.json")
    assert rec["noop_runner_implemented"] is False


# 6. dry_run_execution_started false
def test_dry_run_not_started():
    rec = _load("batch3_p0_implementation_planning_decision_record.json")
    assert rec["dry_run_execution_started"] is False


# 7. monitoring_execution_started false
def test_monitoring_not_started():
    rec = _load("batch3_p0_implementation_planning_decision_record.json")
    assert rec["monitoring_execution_started"] is False


# 8. candidate_review_executed false
def test_candidate_review_not_executed():
    rec = _load("batch3_p0_implementation_planning_decision_record.json")
    assert rec["candidate_review_executed"] is False


# 9. factor_calculation_executed false
def test_factor_calculation_not_executed():
    rec = _load("batch3_p0_implementation_planning_decision_record.json")
    assert rec["factor_calculation_executed"] is False


# 10. factor_results_modified false
def test_factor_results_not_modified():
    rec = _load("batch3_p0_implementation_planning_decision_record.json")
    assert rec["factor_results_modified"] is False


# 11. runtime_reports_modified false
def test_runtime_reports_not_modified():
    rec = _load("batch3_p0_implementation_planning_decision_record.json")
    assert rec["runtime_reports_modified"] is False


# 12. runtime_audit_modified false
def test_runtime_audit_not_modified():
    rec = _load("batch3_p0_implementation_planning_decision_record.json")
    assert rec["runtime_audit_modified"] is False


# 13. external_data_fetch_started false
def test_external_data_not_fetched():
    rec = _load("batch3_p0_implementation_planning_decision_record.json")
    assert rec["external_data_fetch_started"] is False


# 14. promotion_allowed false
def test_promotion_not_allowed():
    rec = _load("batch3_p0_implementation_planning_decision_record.json")
    assert rec["promotion_allowed"] is False


# 15. alpha_claim_allowed false
def test_alpha_claim_not_allowed():
    rec = _load("batch3_p0_implementation_planning_decision_record.json")
    assert rec["alpha_claim_allowed"] is False


# 16. production/broker/real_trade BLOCKED
def test_production_blocked():
    rec = _load("batch3_p0_implementation_planning_decision_record.json")
    assert rec["production"] == "BLOCKED"
    assert rec["broker_runtime"] == "BLOCKED"
    assert rec["real_trade"] == "BLOCKED"


# 17. F26/F27 no auto unlock (conditions)
def test_f26_f27_locked():
    cond = _load("batch3_p0_implementation_branch_conditions.json")
    assert cond["f26_locked"] is True
    assert cond["f27_locked"] is True


# 18. no SkillOS modification (safety audit)
def test_no_skillos_modification():
    sa = _load("batch3_p0_implementation_planning_decision_safety_audit.json")
    assert sa["checks"]["no_skillos_modification"] is True


# 19. no docs/skillos (safety audit)
def test_no_docs_skillos():
    sa = _load("batch3_p0_implementation_planning_decision_safety_audit.json")
    assert sa["checks"]["no_docs_skillos"] is True


# 20. no tests/skillos (safety audit)
def test_no_tests_skillos():
    sa = _load("batch3_p0_implementation_planning_decision_safety_audit.json")
    assert sa["checks"]["no_tests_skillos"] is True


# 21. no pycache (safety audit)
def test_no_pycache():
    sa = _load("batch3_p0_implementation_planning_decision_safety_audit.json")
    assert sa["checks"]["no_pycache"] is True


# 22. no V13_6 (safety audit)
def test_no_v13_6():
    sa = _load("batch3_p0_implementation_planning_decision_safety_audit.json")
    assert sa["checks"]["no_v13_6"] is True


# 23. no tag (safety audit)
def test_no_tag():
    sa = _load("batch3_p0_implementation_planning_decision_safety_audit.json")
    assert sa["checks"]["no_tag"] is True


# 24. next legal entry = CREATE_CONTROLLED_NOOP_DRY_RUN_P0_IMPLEMENTATION_BRANCH_ONLY
def test_next_legal_entry():
    closeout = _load("batch3_p0_implementation_planning_decision_closeout.json")
    assert closeout["next_legal_entry"] == "CREATE_CONTROLLED_NOOP_DRY_RUN_P0_IMPLEMENTATION_BRANCH_ONLY"
    ne = _load("batch3_p0_implementation_planning_next_entry.json")
    assert ne["next_legal_entry"] == "CREATE_CONTROLLED_NOOP_DRY_RUN_P0_IMPLEMENTATION_BRANCH_ONLY"


# Additional: safety audit has 0 violations
def test_safety_audit_zero_violations():
    sa = _load("batch3_p0_implementation_planning_decision_safety_audit.json")
    assert sa["violation_count"] == 0
    assert sa["violations"] == []


# Additional: closeout status correct
def test_closeout_status():
    co = _load("batch3_p0_implementation_planning_decision_closeout.json")
    assert co["status"] == "V13_F5_1_14_P0_IMPLEMENTATION_PLANNING_DECISION_COMPLETE"


# Additional: decision status APPROVED_BY_HUMAN
def test_decision_approved_by_human():
    rec = _load("batch3_p0_implementation_planning_decision_record.json")
    assert rec["decision_status"] == "APPROVED_BY_HUMAN"


# Additional: pipeline signature consistent across all files
def test_pipeline_signature_consistent():
    expected = "V13-F5-1-14-HUMAN-CONTROLLED-NOOP-P0-IMPLEMENTATION-PLANNING-DECISION"
    for name in EXPECTED_FILES:
        d = _load(name)
        assert d["pipeline_signature"] == expected, f"Wrong pipeline_signature in {name}"
