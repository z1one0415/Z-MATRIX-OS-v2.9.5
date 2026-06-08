"""V13.F3.3 — Blueprint tests."""
import json
from pathlib import Path
B = Path(__file__).resolve().parent.parent.parent.parent.parent / "runtime_reports" / "research" / "factors" / "openclaw_batch"
bp = json.loads((B / "v13_f3_3_research_composite_blueprint.json").read_text())
def test_blueprint_only(): assert bp.get("blueprint_only") is True
def test_not_executable(): assert bp.get("composite_formula_executable") is False
def test_no_weights(): assert bp.get("numeric_weights_assigned") is False
def test_readying_f3_4(): assert bp.get("ready_for_f3_4_true_oos_requirement_plan") is True
def test_readying_f3_5(): assert bp.get("ready_for_f3_5_candidate_monitoring_plan") is True
def test_forbidden_outputs(): forbid = bp.get("forbidden_outputs", []); assert "composite_factor_value" in forbid
def test_forbidden_trade(): forbid = bp.get("forbidden_outputs", []); assert "trade_signal" in forbid or "portfolio_weight" in forbid
def test_no_promotion(): assert bp.get("promotion_allowed") is False
def test_no_alpha(): assert bp.get("alpha_claim_allowed") is False
