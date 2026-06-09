"""
V13.F5.1.17 Human Controlled Noop P0 Disabled-Default Review Decision Tests.
"""

import json
from pathlib import Path

R = Path("research/factor_library/reviews/batch_003/f5_1_17_p0_disabled_default_review_decision")
E = [
    "batch3_p0_disabled_default_review_record.json",
    "batch3_p0_disabled_default_review_matrix.json",
    "batch3_p0_disabled_default_code_review_summary.json",
    "batch3_p0_disabled_default_test_review_summary.json",
    "batch3_p0_disabled_default_risk_review.json",
    "batch3_p0_disabled_default_review_safety_audit.json",
    "batch3_p0_disabled_default_review_closeout.json",
    "batch3_p0_disabled_default_next_entry.json",
]

def _l(n): return json.loads((R / n).read_text())

# 1
def test_dir_exists(): assert R.exists()
# 2
def test_8_files(): 
    for f in E: assert (R / f).exists(), f"Missing: {f}"
# 3
def test_decision():
    assert _l("batch3_p0_disabled_default_review_record.json")["decision"] == "GO_FOR_CONTROLLED_NOOP_DRY_RUN_P0_DISABLED_DEFAULT_MERGE_REVIEW"
# 4
def test_merge_not_allowed():
    rec = _l("batch3_p0_disabled_default_review_record.json")
    assert rec["merge_allowed_now"] is False
# 5-16: safety invariants
def test_safety_invariants():
    rec = _l("batch3_p0_disabled_default_review_record.json")
    assert rec["runner_enabled"] is False     # 5
    assert rec["execution_allowed"] is False  # 6
    assert rec["side_effects_allowed"] is False  # 7
    assert rec["dry_run_execution_started"] is False  # 8
    assert rec["monitoring_execution_started"] is False  # 9
    assert rec["candidate_review_executed"] is False  # 10
    assert rec["factor_calculation_executed"] is False  # 11
    assert rec["factor_results_modified"] is False  # 12
    assert rec["runtime_reports_modified"] is False  # 13
    assert rec["runtime_audit_modified"] is False  # 14
    assert rec["external_data_fetch_started"] is False  # 15
    assert rec["production"] == "BLOCKED"     # 16
    assert rec["broker_runtime"] == "BLOCKED"
    assert rec["real_trade"] == "BLOCKED"
# 17
def test_code_review_9_files():
    cr = _l("batch3_p0_disabled_default_code_review_summary.json")
    assert len(cr["source_files"]) == 9
    for sf in cr["source_files"]:
        assert sf["reviewed"] is True
        assert sf["disabled_default_safe"] is True
# 18
def test_test_review_441():
    tr = _l("batch3_p0_disabled_default_test_review_summary.json")
    assert "441 passed" in tr["test_results"]["combined"]
    assert tr["all_passed"] is True
# 19
def test_risk_review_12():
    rr = _l("batch3_p0_disabled_default_risk_review.json")
    assert rr["risk_count"] >= 12
# 20-25：safety audit checks
def test_safety_audit():
    sa = _l("batch3_p0_disabled_default_review_safety_audit.json")
    assert sa["violation_count"] == 0
    assert sa["checks"]["no_skillos_modification"] is True  # 20
    assert sa["checks"]["no_docs_skillos"] is True  # 21
    assert sa["checks"]["no_tests_skillos"] is True  # 22
    assert sa["checks"]["no_pycache"] is True  # 23
    assert sa["checks"]["no_v13_6"] is True  # 24
    assert sa["checks"]["no_tag"] is True  # 25
# 26
def test_next_entry():
    co = _l("batch3_p0_disabled_default_review_closeout.json")
    assert co["next_legal_entry"] == "HUMAN_CONTROLLED_NOOP_DRY_RUN_P0_DISABLED_DEFAULT_MERGE_DECISION_ONLY"
    ne = _l("batch3_p0_disabled_default_next_entry.json")
    assert ne["next_legal_entry"] == "HUMAN_CONTROLLED_NOOP_DRY_RUN_P0_DISABLED_DEFAULT_MERGE_DECISION_ONLY"
# Additional: pipeline signature consistent
def test_pipeline_sig():
    expected = "V13-F5-1-17-HUMAN-CONTROLLED-NOOP-P0-DISABLED-DEFAULT-REVIEW-DECISION"
    for f in E:
        d = _l(f)
        assert d["pipeline_signature"] == expected, f"Wrong in {f}"
# Additional: code review runner_enabled false
def test_code_review_runner_disabled():
    cr = _l("batch3_p0_disabled_default_code_review_summary.json")
    assert cr["special_confirmations"]["runner_enabled"] is False
    assert cr["special_confirmations"]["execution_allowed"] is False
# Additional: risk all accepted
def test_all_risks_accepted():
    rr = _l("batch3_p0_disabled_default_risk_review.json")
    for r in rr["risks"]:
        assert r["review_result"] == "ACCEPTED"
