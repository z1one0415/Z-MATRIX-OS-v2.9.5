"""
V13.F5.1.18 Human Controlled Noop P0 Disabled-Default Merge Decision Tests.
"""
import json
from pathlib import Path

M = Path("research/factor_library/reviews/batch_003/f5_1_18_p0_disabled_default_merge_decision")
E = [f"batch3_p0_disabled_default_merge_{s}.json" for s in [
    "decision_record","lineage_audit","scope","readiness_matrix",
    "risk_register","safety_audit","test_summary","closeout","next_entry"
]]
def _l(n): return json.loads((M / n).read_text())

# 1
def test_dir(): assert M.exists()
# 2
def test_9_files():
    for f in E: assert (M / f).exists()
# 3
def test_merge_not_executed():
    co = _l("batch3_p0_disabled_default_merge_closeout.json")
    assert co["merge_executed"] is False
# 4-8 safety
def test_safety():
    co = _l("batch3_p0_disabled_default_merge_closeout.json")
    assert co["runner_enabled"] is False      # 4
    assert co["execution_allowed"] is False   # 5
    assert co["dry_run_execution_started"] is False  # 6
    assert co["runtime_reports_modified"] is False   # 7
    assert co["runtime_audit_modified"] is False     # 8
# 9
def test_prod_blocked():
    co = _l("batch3_p0_disabled_default_merge_closeout.json")
    assert co["production"] == "BLOCKED"
    assert co["broker_runtime"] == "BLOCKED"
    assert co["real_trade"] == "BLOCKED"
# 10-13 lineage
def test_lineage_audit():
    la = _l("batch3_p0_disabled_default_merge_lineage_audit.json")
    assert la["target_contains_polluted_commits"] is True      # 10
    assert la["source_contains_polluted_commits"] is False     # 11
    assert len(la["polluted_commits_invalidated"]) == 3        # 12
    assert la["lineage_decision"] == "TARGET_LINEAGE_REPAIR_REQUIRED"  # 13
# 14-17 merge scope
def test_merge_scope():
    sc = _l("batch3_p0_disabled_default_merge_scope.json")
    blocked = sc["blocked_merge_content"]
    assert any("docs/skillos" in b for b in blocked)    # 14
    assert any("skillos/**" == b for b in blocked)      # 15
    assert any("tests/skillos" in b for b in blocked)   # 16
    assert any("pycache" in b for b in blocked)         # 17
# 18-19
def test_safety_audit():
    sa = _l("batch3_p0_disabled_default_merge_safety_audit.json")
    assert sa["checks"]["no_merge_executed"] is True    # 18
    assert sa["checks"]["target_lineage_checked"] is True
# 19
def test_next_entry():
    co = _l("batch3_p0_disabled_default_merge_closeout.json")
    assert co["next_legal_entry"] == "RESTORE_CLEAN_TARGET_LINEAGE_BEFORE_MERGE_ONLY"
    ne = _l("batch3_p0_disabled_default_merge_next_entry.json")
    assert ne["next_legal_entry"] == "RESTORE_CLEAN_TARGET_LINEAGE_BEFORE_MERGE_ONLY"
# 20-21
def test_safety_no_v13_6_no_tag():
    sa = _l("batch3_p0_disabled_default_merge_safety_audit.json")
    assert sa["checks"]["no_v13_6"] is True
    assert sa["checks"]["no_tag"] is True
# Additional
def test_decision_polluted():
    rec = _l("batch3_p0_disabled_default_merge_decision_record.json")
    assert rec["target_lineage_repair_required"] is True
    assert rec["merge_approval_granted"] is False
    assert rec["target_head_is_polluted"] is True
def test_readiness_has_blocked():
    rm = _l("batch3_p0_disabled_default_merge_readiness_matrix.json")
    blocked_items = [i for i in rm["items"] if "BLOCKED" in i["status"]]
    assert len(blocked_items) >= 1
def test_risk_blocking_active():
    rr = _l("batch3_p0_disabled_default_merge_risk_register.json")
    blocking = [r for r in rr["risks"] if r["status"] == "ACTIVE_BLOCKING"]
    assert len(blocking) >= 1
