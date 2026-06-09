"""
V13.F5.1.19 Restore Clean Target Lineage Before Merge Tests.
"""
import json
from pathlib import Path

R = Path("research/factor_library/reviews/batch_003/f5_1_19_target_lineage_restoration")
E = [
    "target_lineage_restoration_overview.json",
    "target_lineage_pollution_audit.json",
    "target_lineage_restoration_decision.json",
    "target_lineage_restoration_scope.json",
    "target_lineage_restoration_safety_audit.json",
    "target_lineage_restoration_closeout.json",
    "target_lineage_restoration_next_entry.json",
]
def _l(n): return json.loads((R / n).read_text())

# 1-2
def test_dir(): assert R.exists()
def test_7_files():
    for f in E: assert (R / f).exists()
# 3-5
def test_lineage():
    aud = _l("target_lineage_pollution_audit.json")
    assert aud["polluted_target_head"] == "0c2e6553d819d790a4c10e90acc111d3e8eb9da6"  # 3
    assert aud["clean_base"] == "4dd8e86ff391e0af9e55de46ae3c93545798336c"          # 4
    assert aud["source_commit_ready"] == "1b291cc"                                   # 5
# 6
def test_invalid_4():
    aud = _l("target_lineage_pollution_audit.json")
    inv = [c["sha"] for c in aud["invalidated_commits"]]
    assert "0c2e6553d819d790a4c10e90acc111d3e8eb9da6" in inv
    assert "a6c3ff25b943277aa70a104373ead26e29e2199d" in inv
    assert "a622b3d921aebc513bcde98d1ade1be09120c131" in inv
    assert any("9f5f3f4" in c for c in inv)
# 7-11
def test_safety():
    co = _l("target_lineage_restoration_closeout.json")
    assert co["merge_executed"] is False              # 7
    assert co["runner_enabled"] is False              # 8
    assert co["execution_allowed"] is False           # 9
    assert co["dry_run_execution_started"] is False   # 10
    assert co["production"] == "BLOCKED"              # 11
    assert co["broker_runtime"] == "BLOCKED"
    assert co["real_trade"] == "BLOCKED"
# 12
def test_next():
    co = _l("target_lineage_restoration_closeout.json")
    assert co["next_legal_entry"] == "HUMAN_REVIEW_RESTORED_TARGET_BEFORE_MERGE_ONLY"
# 13-18
def test_clean_audit():
    sa = _l("target_lineage_restoration_safety_audit.json")
    assert sa["checks"]["no_skillos_modification"] is True   # 13
    assert sa["checks"]["no_docs_skillos"] is True           # 14
    assert sa["checks"]["no_tests_skillos"] is True          # 15
    assert sa["checks"]["no_pycache"] is True                # 16
    assert sa["checks"]["no_v13_6"] is True                  # 17
    assert sa["checks"]["no_tag"] is True                    # 18
# Additional
def test_strategy():
    ov = _l("target_lineage_restoration_overview.json")
    assert ov["chosen_strategy"] == "CREATE_CLEAN_TARGET_BRANCH"
    assert ov["clean_target_branch"] == "v4.0-batch-0-final-hardgates-scope-lock-clean"
def test_original_preserved():
    ov = _l("target_lineage_restoration_overview.json")
    assert "polluted" in ov["polluted_target_branch"] or "lock" in ov["polluted_target_branch"]
    # Original polluted branch name recorded (may or may not contain "polluted" literally)
    assert len(ov["polluted_target_branch"]) > 20
