"""
V13.F5.1.18.1 Clean Rebuild Human P0 Disabled-Default Merge Decision Tests.

Verifies merge decision AND confirms F5.1.16 files remain intact (not regressed).
"""
import json
from pathlib import Path

M = Path("research/factor_library/reviews/batch_003/f5_1_18_p0_disabled_default_merge_decision")
F16 = Path("research/factor_library/reviews/batch_003/f5_1_16_p0_disabled_default_implementation")
E = [f"batch3_p0_disabled_default_merge_{s}.json" for s in [
    "decision_record","lineage_audit","scope","readiness_matrix",
    "risk_register","safety_audit","test_summary","closeout","next_entry"
]]
def _l(p, n): return json.loads((p / n).read_text())

# 1
def test_dir(): assert M.exists()
# 2
def test_9_files():
    for f in E: assert (M / f).exists()
# 3
def test_decision():
    assert _l(M, "batch3_p0_disabled_default_merge_decision_record.json")["decision"] == "HOLD_MERGE_FOR_TARGET_LINEAGE_REPAIR"
# 4-6
def test_merge_blocked():
    rec = _l(M, "batch3_p0_disabled_default_merge_closeout.json")
    assert rec["merge_executed"] is False         # 4
    assert rec["merge_approval_granted"] is False # 5
    assert rec["target_lineage_repair_required"] is True  # 6
# 7-8
def test_lineage():
    la = _l(M, "batch3_p0_disabled_default_merge_lineage_audit.json")
    assert la["target_head"] == "0c2e6553d819d790a4c10e90acc111d3e8eb9da6"  # 7
    assert la["target_head_is_polluted_commit"] is True  # 8
# 9
def test_source_clean():
    la = _l(M, "batch3_p0_disabled_default_merge_lineage_audit.json")
    assert la["source_contains_polluted_commits"] is False  # 9
# 10
def test_next_entry():
    co = _l(M, "batch3_p0_disabled_default_merge_closeout.json")
    assert co["next_legal_entry"] == "RESTORE_CLEAN_TARGET_LINEAGE_BEFORE_MERGE_ONLY"  # 10
# 11-14
def test_safety():
    co = _l(M, "batch3_p0_disabled_default_merge_closeout.json")
    assert co["runner_enabled"] is False            # 11
    assert co["execution_allowed"] is False         # 12
    assert co["dry_run_execution_started"] is False  # 13
    assert co["production"] == "BLOCKED"            # 14
    assert co["broker_runtime"] == "BLOCKED"
    assert co["real_trade"] == "BLOCKED"
# 15-17
def test_skillos_blocked():
    sa = _l(M, "batch3_p0_disabled_default_merge_safety_audit.json")
    assert sa["checks"]["no_skillos_modification"] is True  # 15
    assert sa["checks"]["no_docs_skillos"] is True          # 16
    assert sa["checks"]["no_tests_skillos"] is True         # 17
# 18-20
def test_pycache_v13_tag():
    sa = _l(M, "batch3_p0_disabled_default_merge_safety_audit.json")
    assert sa["checks"]["no_pycache"] is True   # 18
    assert sa["checks"]["no_v13_6"] is True     # 19
    assert sa["checks"]["no_tag"] is True       # 20
# 21
def test_f5_1_16_closeout_intact():
    co = _l(F16, "batch3_p0_disabled_default_closeout.json")
    assert co.get("full_test_gate_status") == "V13_F5_1_16_2_FULL_TEST_GATE_CLOSED"
# 22
def test_f5_1_16_safety_intact():
    sa = _l(F16, "batch3_p0_disabled_default_safety_audit.json")
    assert sa.get("full_test_gate_checked") is True
    assert sa.get("boundary_reconciliation_checked") is True
# 23
def test_f5_1_16_test_report_intact():
    tr = _l(F16, "batch3_p0_disabled_default_test_report.json")
    assert tr.get("full_test_gate_closed") is True
    assert tr.get("interface_tests_run") is True
# 24
def test_f5_1_16_test_report_not_regressed():
    tr = _l(F16, "batch3_p0_disabled_default_test_report.json")
    combined = tr.get("full_test_result", {}).get("combined", "")
    assert "441 passed" in combined, f"Expected 441 passed, got: {combined}"
# 25
def test_invalidated_9f5f3f4_recorded():
    co = _l(M, "batch3_p0_disabled_default_merge_closeout.json")
    assert "9f5f3f4" in co.get("invalidated_commit", "")
# 26-28: additional clean rebuild marks
def test_clean_rebuild_chain():
    la = _l(M, "batch3_p0_disabled_default_merge_lineage_audit.json")
    chain = la["clean_rebuild_chain"]
    assert "33dfe73" in chain
    assert "4dd8e86" in chain
def test_merge_scope_blocks_skillos():
    sc = _l(M, "batch3_p0_disabled_default_merge_scope.json")
    blocked = sc["blocked_merge_content"]
    assert any("skillos" in b for b in blocked)
def test_readiness_has_blocked():
    rm = _l(M, "batch3_p0_disabled_default_merge_readiness_matrix.json")
    blocked = [i for i in rm["items"] if "BLOCKED" in i["status"]]
    assert len(blocked) >= 2
def test_risk_active_blocking():
    rr = _l(M, "batch3_p0_disabled_default_merge_risk_register.json")
    active = [r for r in rr["risks"] if r["status"] == "ACTIVE_BLOCKING"]
    assert len(active) >= 1
