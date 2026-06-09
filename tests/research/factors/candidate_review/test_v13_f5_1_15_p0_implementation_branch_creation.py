"""
V13.F5.1.15 Create Controlled Noop Dry-Run P0 Implementation Branch Tests.

Verifies:
- Branch creation directory and 6 seal files exist
- Source decision commit exact
- Branch ref exact
- All safety invariants maintained
- No implementation, no execution, no side effects
- Next entry = CONTROLLED_NOOP_DRY_RUN_P0_DISABLED_DEFAULT_IMPLEMENTATION_ONLY
"""

import json
from pathlib import Path

BRANCH_DIR = Path(
    "research/factor_library/reviews/batch_003/f5_1_15_p0_implementation_branch_creation"
)

EXPECTED_FILES = [
    "batch3_p0_implementation_branch_creation_overview.json",
    "batch3_p0_implementation_branch_lineage_seal.json",
    "batch3_p0_implementation_branch_scope.json",
    "batch3_p0_implementation_branch_safety_audit.json",
    "batch3_p0_implementation_branch_readiness.json",
    "batch3_p0_implementation_branch_closeout.json",
]

SOURCE_DECISION_COMMIT = "5a5701441358fac30b726f828340fb70f5a07c67"
BRANCH_REF = "impl/research-batch3-controlled-noop-dry-run-p0-implementation-clean"


def _load(name: str) -> dict:
    return json.loads((BRANCH_DIR / name).read_text())


# 1. Branch creation directory exists
def test_branch_creation_directory_exists():
    assert BRANCH_DIR.exists()
    assert BRANCH_DIR.is_dir()


# 2. All 6 seal files exist
def test_6_seal_files_exist():
    for name in EXPECTED_FILES:
        assert (BRANCH_DIR / name).exists(), f"Missing: {name}"


# 3. Source decision commit exact
def test_source_decision_commit():
    closeout = _load("batch3_p0_implementation_branch_closeout.json")
    assert closeout["source_decision_commit"] == SOURCE_DECISION_COMMIT


# 4. Branch ref exact
def test_branch_ref():
    closeout = _load("batch3_p0_implementation_branch_closeout.json")
    assert closeout["branch"] == BRANCH_REF


# 5. implementation_started false
def test_implementation_not_started():
    closeout = _load("batch3_p0_implementation_branch_closeout.json")
    assert closeout["implementation_started"] is False


# 6. noop_runner_implemented false
def test_noop_runner_not_implemented():
    closeout = _load("batch3_p0_implementation_branch_closeout.json")
    assert closeout["noop_runner_implemented"] is False


# 7. dry_run_execution_started false
def test_dry_run_not_started():
    closeout = _load("batch3_p0_implementation_branch_closeout.json")
    assert closeout["dry_run_execution_started"] is False


# 8. monitoring_execution_started false
def test_monitoring_not_started():
    closeout = _load("batch3_p0_implementation_branch_closeout.json")
    assert closeout["monitoring_execution_started"] is False


# 9. candidate_review_executed false
def test_candidate_review_not_executed():
    closeout = _load("batch3_p0_implementation_branch_closeout.json")
    assert closeout["candidate_review_executed"] is False


# 10. factor_calculation_executed false
def test_factor_calculation_not_executed():
    closeout = _load("batch3_p0_implementation_branch_closeout.json")
    assert closeout["factor_calculation_executed"] is False


# 11. factor_results_modified false
def test_factor_results_not_modified():
    closeout = _load("batch3_p0_implementation_branch_closeout.json")
    assert closeout["factor_results_modified"] is False


# 12. runtime_reports_modified false
def test_runtime_reports_not_modified():
    closeout = _load("batch3_p0_implementation_branch_closeout.json")
    assert closeout["runtime_reports_modified"] is False


# 13. runtime_audit_modified false
def test_runtime_audit_not_modified():
    closeout = _load("batch3_p0_implementation_branch_closeout.json")
    assert closeout["runtime_audit_modified"] is False


# 14. production/broker/real_trade BLOCKED
def test_production_blocked():
    closeout = _load("batch3_p0_implementation_branch_closeout.json")
    assert closeout["production"] == "BLOCKED"
    assert closeout["broker_runtime"] == "BLOCKED"
    assert closeout["real_trade"] == "BLOCKED"


# 15. no SkillOS modification
def test_no_skillos_modification():
    sa = _load("batch3_p0_implementation_branch_safety_audit.json")
    assert sa["checks"]["no_skillos_modification"] is True


# 16. no docs/skillos
def test_no_docs_skillos():
    sa = _load("batch3_p0_implementation_branch_safety_audit.json")
    assert sa["checks"]["no_docs_skillos"] is True


# 17. no tests/skillos
def test_no_tests_skillos():
    sa = _load("batch3_p0_implementation_branch_safety_audit.json")
    assert sa["checks"]["no_tests_skillos"] is True


# 18. no pycache
def test_no_pycache():
    sa = _load("batch3_p0_implementation_branch_safety_audit.json")
    assert sa["checks"]["no_pycache"] is True


# 19. no V13_6
def test_no_v13_6():
    sa = _load("batch3_p0_implementation_branch_safety_audit.json")
    assert sa["checks"]["no_v13_6"] is True


# 20. no tag
def test_no_tag():
    sa = _load("batch3_p0_implementation_branch_safety_audit.json")
    assert sa["checks"]["no_tag"] is True


# 21. next legal entry = CONTROLLED_NOOP_DRY_RUN_P0_DISABLED_DEFAULT_IMPLEMENTATION_ONLY
def test_next_legal_entry():
    closeout = _load("batch3_p0_implementation_branch_closeout.json")
    assert closeout["next_legal_entry"] == "CONTROLLED_NOOP_DRY_RUN_P0_DISABLED_DEFAULT_IMPLEMENTATION_ONLY"


# Additional: lineage seal has trusted chain
def test_lineage_seal_trusted_chain():
    seal = _load("batch3_p0_implementation_branch_lineage_seal.json")
    assert seal["lineage_verified"] is True
    assert seal["branch_created_from_trusted_chain"] is True
    assert seal["no_polluted_ancestry"] is True
    assert "5a57014" in seal["trusted_chain"]


# Additional: old polluted commits listed
def test_old_polluted_commits_listed():
    seal = _load("batch3_p0_implementation_branch_lineage_seal.json")
    assert "0c2e655" in seal["old_polluted_commits"]
    assert "a6c3ff2" in seal["old_polluted_commits"]
    assert "a622b3d" in seal["old_polluted_commits"]


# Additional: safety audit 0 violations
def test_safety_audit_zero_violations():
    sa = _load("batch3_p0_implementation_branch_safety_audit.json")
    assert sa["violation_count"] == 0
    assert sa["violations"] == []


# Additional: pipeline signature consistent
def test_pipeline_signature_consistent():
    expected = "V13-F5-1-15-CREATE-CONTROLLED-NOOP-DRY-RUN-P0-IMPLEMENTATION-BRANCH"
    for name in EXPECTED_FILES:
        d = _load(name)
        assert d["pipeline_signature"] == expected, f"Wrong in {name}"
