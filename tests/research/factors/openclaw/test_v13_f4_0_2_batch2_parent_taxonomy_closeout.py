"""V13.F4.0.2 — Taxonomy closeout tests."""
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent.parent.parent.parent
B2 = ROOT / "runtime_reports" / "research" / "factors" / "openclaw_batch_2"
co = json.loads((B2 / "v13_f4_0_2_batch2_parent_taxonomy_closeout.json").read_text())
def test_pass(): assert "PASS" in co.get("status", "")
def test_executed(): assert co.get("canonicalization_executed") is True
def test_cov_fixed(): assert co.get("coverage_fail_pass_conflict_fixed") is True
def test_lane_consistent(): assert co.get("lane_count_consistency_passed") is True
def test_source_audit_fixed(): assert co.get("source_audit_group_taxonomy_fixed") is True
def test_pass_5(): assert len(co.get("pass_research_evidence_factors", [])) == 5
def test_f09_violated(): assert "VIOLATED" in co.get("f09_status", "")
def test_f17_group(): assert "COMPLETED" in co.get("f17_f20_group_status", "")
def test_no_promotion(): assert co.get("ready_for_promotion_review") == []
def test_frozen_preserved(): assert co.get("frozen_candidates_preserved") == ["F04","F10","F11"]
def test_no_f3_5_1(): assert co.get("f3_5_1_monitoring_execution_executed") is False
def test_no_f3_6(): assert co.get("f3_6_true_oos_validation_executed") is False
def test_no_composite(): assert co.get("multi_factor_composite_built") is False
def test_no_alpha(): assert co.get("alpha_claim_allowed") is False
def test_prod_blocked(): assert co.get("production") == "BLOCKED"
def test_next(): assert co.get("recommended_next_action") == "PREPARE_V13_F4_1_BATCH2_CANDIDATE_REVIEW"
