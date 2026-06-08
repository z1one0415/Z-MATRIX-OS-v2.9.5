"""V13.F4.0.1 — Repair closeout tests."""
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent.parent.parent.parent
B2 = ROOT / "runtime_reports" / "research" / "factors" / "openclaw_batch_2"
co = json.loads((B2 / "v13_f4_0_1_batch2_repair_closeout.json").read_text())
def test_pass(): assert "PASS" in co.get("status", "")
def test_repair_executed(): assert co.get("repair_executed") is True
def test_coverage_fixed(): assert co.get("coverage_fail_pass_conflict_fixed") is True
def test_lane_fixed(): assert co.get("source_audit_contract_violation_fixed") is True
def test_no_promotion(): assert co.get("ready_for_promotion_review") == []
def test_no_composite(): assert co.get("multi_factor_composite_built") is False
def test_no_weight(): assert co.get("weight_optimization_executed") is False
def test_no_v13_6(): assert co.get("v13_6_allowed") is False
def test_no_alpha(): assert co.get("alpha_claim_allowed") is False
def test_prod_blocked(): assert co.get("production") == "BLOCKED"
def test_next_action(): assert len(co.get("recommended_next_action", "")) > 0
