"""V13.F3.1 — Closeout tests."""
import json
from pathlib import Path
BATCH = Path(__file__).resolve().parent.parent.parent.parent.parent / "runtime_reports" / "research" / "factors" / "openclaw_batch"
co = json.loads((BATCH / "v13_f3_1_candidate_review_closeout.json").read_text())
def test_review_executed(): assert co.get("candidate_review_executed") is True
def test_reviewed_3(): assert co.get("reviewed_factors") == ["F04", "F10", "F11"]
def test_no_promotion(): assert co.get("ready_for_promotion_review") == []
def test_no_promotion_allowed(): assert co.get("promotion_review_allowed") is False
def test_no_composite(): assert co.get("multi_factor_composite_built") is False
def test_no_weight_opt(): assert co.get("weight_optimization_executed") is False
def test_no_oos(): assert co.get("oos_alpha_validation_executed") is False
def test_no_v13_6(): assert co.get("v13_6_allowed") is False
def test_no_paper(): assert co.get("paper_trading_allowed") is False
def test_no_alpha(): assert co.get("alpha_claim_allowed") is False
def test_prod_blocked(): assert co.get("production") == "BLOCKED"
def test_broker_blocked(): assert co.get("broker_runtime") == "BLOCKED"
def test_real_trade_blocked(): assert co.get("real_trade") == "BLOCKED"
def test_next_action(): assert len(co.get("recommended_next_action", "")) > 0
