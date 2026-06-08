"""V13.F3.3 — Closeout tests."""
import json
from pathlib import Path
B = Path(__file__).resolve().parent.parent.parent.parent.parent / "runtime_reports" / "research" / "factors" / "openclaw_batch"
co = json.loads((B / "v13_f3_3_research_composite_design_closeout.json").read_text())
def test_pass(): assert "PASS" in co.get("status", ""); assert co.get("design_executed") is True
def test_blueprint_only(): assert co.get("blueprint_only") is True
def test_3_factors(): assert co.get("component_factors") == ["F04","F10","F11"]
def test_no_panel(): assert co.get("composite_panel_generated") is False
def test_no_weights(): assert co.get("numeric_weights_assigned") is False
def test_no_weight_opt(): assert co.get("weight_optimization_executed") is False
def test_no_factor_value(): assert co.get("composite_factor_value_generated") is False
def test_no_trade_signal(): assert co.get("trade_signal_generated") is False
def test_no_position(): assert co.get("position_generated") is False
def test_no_order(): assert co.get("order_generated") is False
def test_no_broker(): assert co.get("broker_instruction_generated") is False
def test_ready_f3_4(): assert co.get("ready_for_f3_4_true_oos_requirement_plan") is True
def test_ready_f3_5(): assert co.get("ready_for_f3_5_candidate_monitoring_plan") is True
def test_no_promotion(): assert co.get("ready_for_promotion_review") == []
def test_no_composite(): assert co.get("multi_factor_composite_built") is False
def test_no_skillos(): assert co.get("skillos_protocol_modified") is False
def test_no_v13_6(): assert co.get("v13_6_allowed") is False
def test_no_paper(): assert co.get("paper_trading_allowed") is False
def test_no_alpha(): assert co.get("alpha_claim_allowed") is False
def test_prod_blocked(): assert co.get("production") == "BLOCKED"
def test_broker_blocked(): assert co.get("broker_runtime") == "BLOCKED"
def test_real_trade_blocked(): assert co.get("real_trade") == "BLOCKED"
def test_next_action(): assert co.get("recommended_next_action") == "PREPARE_V13_F3_4_TRUE_OOS_REQUIREMENT_PLAN"
