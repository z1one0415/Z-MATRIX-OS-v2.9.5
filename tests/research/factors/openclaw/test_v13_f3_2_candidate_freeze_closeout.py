"""V13.F3.2 — Freeze closeout tests."""
import json
from pathlib import Path
B = Path(__file__).resolve().parent.parent.parent.parent.parent / "runtime_reports" / "research" / "factors" / "openclaw_batch"
co = json.loads((B / "v13_f3_2_candidate_freeze_closeout.json").read_text())
def test_pass(): assert "PASS" in co.get("status", "")
def test_executed(): assert co.get("candidate_freeze_executed") is True
def test_3_frozen(): assert co.get("frozen_candidate_count") == 3
def test_f04_frozen(): assert co.get("f04_freeze_status") == "FROZEN_CANDIDATE"
def test_f10_frozen(): assert "REGIME" in co.get("f10_freeze_status", "")
def test_f11_frozen(): assert "TACTICAL" in co.get("f11_freeze_status", "")
def test_ready_3_3(): assert "F04" in co.get("ready_for_f3_3_research_composite_design", [])
def test_no_promotion(): assert co.get("ready_for_promotion_review") == []
def test_promotion_not_allowed(): assert co.get("promotion_review_allowed") is False
def test_composite_not_built(): assert co.get("multi_factor_composite_built") is False
def test_composite_design_allowed(): assert co.get("multi_factor_composite_design_allowed_next") is True
def test_weight_not_executed(): assert co.get("weight_optimization_executed") is False
def test_oos_not_executed(): assert co.get("oos_alpha_validation_executed") is False
def test_v13_6_false(): assert co.get("v13_6_allowed") is False
def test_paper_false(): assert co.get("paper_trading_allowed") is False
def test_alpha_false(): assert co.get("alpha_claim_allowed") is False
def test_prod_blocked(): assert co.get("production") == "BLOCKED"
def test_broker_blocked(): assert co.get("broker_runtime") == "BLOCKED"
def test_real_trade_blocked(): assert co.get("real_trade") == "BLOCKED"
def test_next_action(): assert co.get("recommended_next_action") == "PREPARE_V13_F3_3_RESEARCH_COMPOSITE_DESIGN"
