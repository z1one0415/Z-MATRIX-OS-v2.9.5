"""V13.F3.4 — Closeout tests."""
import json
from pathlib import Path
B = Path(__file__).resolve().parent.parent.parent.parent.parent / "runtime_reports" / "research" / "factors" / "openclaw_batch"
co = json.loads((B / "v13_f3_4_true_oos_requirement_closeout.json").read_text())
def test_pass(): assert "PASS" in co.get("status", "")
def test_executed(): assert co.get("requirement_plan_executed") is True
def test_no_oos_exec(): assert co.get("true_oos_validation_executed") is False
def test_no_label_gen(): assert co.get("oos_label_generation_executed") is False
def test_min_6(): assert co.get("minimum_true_oos_months_required") == 6
def test_pref_12(): assert co.get("preferred_true_oos_months_required") == 12
def test_blocked(): assert co.get("same_sample_promotion_blocked") is True
def test_label_planned(): assert co.get("oos_outcome_label_isolation_planned") is True
def test_gate_planned(): assert co.get("gate_label_requirements_planned") is True
def test_criteria_built(): assert co.get("per_factor_acceptance_criteria_built") is True
def test_ready_f3_5(): assert co.get("ready_for_f3_5_candidate_monitoring_plan") is True
def test_not_ready_f3_6(): assert co.get("ready_for_f3_6_true_oos_validation_execution") is False
def test_no_promotion(): assert co.get("ready_for_promotion_review") == []
def test_no_composite(): assert co.get("composite_execution_executed") is False
def test_no_panel(): assert co.get("composite_panel_generated") is False
def test_no_weight(): assert co.get("weight_optimization_executed") is False
def test_no_v13_6(): assert co.get("v13_6_allowed") is False
def test_no_alpha(): assert co.get("alpha_claim_allowed") is False
def test_prod_blocked(): assert co.get("production") == "BLOCKED"
def test_next_action(): assert co.get("recommended_next_action") == "PREPARE_V13_F3_5_CANDIDATE_MONITORING_PLAN"
