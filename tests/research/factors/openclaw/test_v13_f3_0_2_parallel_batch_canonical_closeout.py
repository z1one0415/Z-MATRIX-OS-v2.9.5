"""V13.F3.0.2 — Canonical closeout tests."""
import json
from pathlib import Path
BATCH = Path(__file__).resolve().parent.parent.parent.parent.parent / "runtime_reports" / "research" / "factors" / "openclaw_batch"
co = json.loads((BATCH / "v13_f3_0_2_parallel_batch_canonical_closeout.json").read_text())
def test_pass(): assert "PASS" in co.get("status", "")
def test_canonicalization_executed(): assert co.get("canonicalization_executed") is True
def test_no_materialization_rerun(): assert co.get("materialization_rerun_executed") is False
def test_no_validation_rerun(): assert co.get("single_factor_validation_rerun_executed") is False
def test_inconsistent_0(): assert co.get("inconsistent_factor_count_after_repair") == 0
def test_pass_3(): assert len(co.get("pass_research_evidence_after_repair", [])) == 3
def test_hypothesis(): assert "F03R" in co.get("hypothesis_only_factors", [])
def test_blocked_4(): assert len(co.get("blocked_by_sample_factors", [])) == 4
def test_ready_next(): assert co.get("ready_for_next_validation") == ["F04", "F10", "F11"]
def test_promotion_empty(): assert co.get("ready_for_promotion_review") == []
def test_multi_composite_false(): assert co.get("multi_factor_composite_built") is False
def test_oos_not_executed(): assert co.get("oos_alpha_validation_executed") is False
def test_skillos_unchanged(): assert co.get("skillos_protocol_modified") is False
def test_v13_6_false(): assert co.get("v13_6_allowed") is False
def test_paper_false(): assert co.get("paper_trading_allowed") is False
def test_alpha_false(): assert co.get("alpha_claim_allowed") is False
def test_ready_alpha_false(): assert co.get("ready_for_alpha_claim") is False
def test_alpha_validated_false(): assert co.get("alpha_validated") is False
def test_prod_blocked(): assert co.get("production") == "BLOCKED"
def test_broker_blocked(): assert co.get("broker_runtime") == "BLOCKED"
def test_real_trade_blocked(): assert co.get("real_trade") == "BLOCKED"
def test_next_action(): assert len(co.get("recommended_next_action", "")) > 0
