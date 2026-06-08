"""V13.F3.4.1 — Closeout tests."""
import json
from pathlib import Path
B = Path(__file__).resolve().parent.parent.parent.parent.parent / "runtime_reports" / "research" / "factors" / "openclaw_batch"
co = json.loads((B / "v13_f3_4_1_oos_boundary_canonicalization_closeout.json").read_text())
def test_pass(): assert "PASS" in co.get("status", "")
def test_executed(): assert co.get("boundary_canonicalization_executed") is True
def test_resolved(): assert co.get("all_last_in_sample_dates_resolved") is True
def test_no_na(): assert co.get("any_na_last_in_sample_date") is False
def test_max_date_non_empty(): assert len(co.get("max_last_in_sample_rebalance_date", "")) > 0
def test_oos_start_non_empty(): assert len(co.get("minimum_oos_start_exclusive", "")) > 0
def test_no_oos(): assert co.get("true_oos_validation_executed") is False
def test_no_label(): assert co.get("oos_label_generation_executed") is False
def test_ready_f3_5(): assert co.get("ready_for_f3_5_candidate_monitoring_plan") is True
def test_not_ready_f3_6(): assert co.get("ready_for_f3_6_true_oos_validation_execution") is False
def test_no_promotion(): assert co.get("ready_for_promotion_review") == []
def test_no_composite(): assert co.get("composite_execution_executed") is False
def test_no_panel(): assert co.get("composite_panel_generated") is False
def test_no_weight(): assert co.get("weight_optimization_executed") is False
def test_no_v13_6(): assert co.get("v13_6_allowed") is False
def test_no_alpha(): assert co.get("alpha_claim_allowed") is False
def test_prod_blocked(): assert co.get("production") == "BLOCKED"
def test_next_action(): assert "PREPARE_V13_F3_5" in co.get("recommended_next_action", "")
