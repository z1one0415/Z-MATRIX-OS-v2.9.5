"""V13.F3.5 — Closeout tests."""
import json
from pathlib import Path
B = Path(__file__).resolve().parent.parent.parent.parent.parent / "runtime_reports" / "research" / "factors" / "openclaw_batch"
co = json.loads((B / "v13_f3_5_candidate_monitoring_plan_closeout.json").read_text())
def test_pass(): assert "PASS" in co.get("status", "")
def test_executed(): assert co.get("monitoring_plan_executed") is True
def test_no_mon_exec(): assert co.get("monitoring_execution_executed") is False
def test_scope(): assert co.get("candidate_scope") == ["F04","F10","F11"]
def test_no_oos_exec(): assert co.get("true_oos_validation_executed") is False
def test_no_label(): assert co.get("oos_label_generation_executed") is False
def test_no_composite(): assert co.get("composite_execution_executed") is False
def test_no_panel(): assert co.get("composite_panel_generated") is False
def test_no_weight(): assert co.get("weight_optimization_executed") is False
def test_no_promotion(): assert co.get("ready_for_promotion_review") == []
def test_no_v13_6(): assert co.get("v13_6_allowed") is False
def test_no_alpha(): assert co.get("alpha_claim_allowed") is False
def test_prod_blocked(): assert co.get("production") == "BLOCKED"
def test_broker_blocked(): assert co.get("broker_runtime") == "BLOCKED"
def test_real_trade_blocked(): assert co.get("real_trade") == "BLOCKED"
def test_next_action(): assert len(co.get("recommended_next_action", "")) > 0
