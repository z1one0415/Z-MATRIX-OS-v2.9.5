"""V13.F4.0 — Closeout tests."""
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent.parent.parent.parent
B2 = ROOT / "runtime_reports" / "research" / "factors" / "openclaw_batch_2"
co = json.loads((B2 / "v13_f4_0_batch2_closeout.json").read_text())
def test_pass(): assert "PASS" in co.get("status", "")
def test_executed(): assert co.get("batch2_orchestration_executed") is True
def test_frozen_preserved(): assert co.get("frozen_candidates_preserved") == ["F04","F10","F11"]
def test_no_mutation(): assert co.get("frozen_candidates_mutated") is False
def test_no_f3_5_1(): assert co.get("f3_5_1_monitoring_execution_executed") is False
def test_no_f3_6(): assert co.get("f3_6_true_oos_validation_executed") is False
def test_pass_factors(): assert len(co.get("pass_research_evidence_factors", [])) >= 6
def test_source_audit(): assert len(co.get("source_audit_only_completed", [])) == 4
def test_candidate_review(): assert len(co.get("ready_for_candidate_review", [])) >= 6
def test_no_promotion(): assert co.get("ready_for_promotion_review") == []
def test_no_composite(): assert co.get("multi_factor_composite_built") is False
def test_no_weight(): assert co.get("weight_optimization_executed") is False
def test_no_v13_6(): assert co.get("v13_6_allowed") is False
def test_no_alpha(): assert co.get("alpha_claim_allowed") is False
def test_prod_blocked(): assert co.get("production") == "BLOCKED"
def test_broker_blocked(): assert co.get("broker_runtime") == "BLOCKED"
def test_real_trade_blocked(): assert co.get("real_trade") == "BLOCKED"
def test_next_action(): assert len(co.get("recommended_next_action", "")) > 0
