"""V13.F3.3 — Contract tests."""
import json
from pathlib import Path
B = Path(__file__).resolve().parent.parent.parent.parent.parent / "runtime_reports" / "research" / "factors" / "openclaw_batch"
c = json.loads((B / "v13_f3_3_research_composite_design_contract.json").read_text())
def test_design_only(): assert c.get("design_only") is True
def test_no_composite_exec(): assert c.get("composite_execution_allowed") is False
def test_no_panel_gen(): assert c.get("composite_panel_generation_allowed") is False
def test_no_weight_opt(): assert c.get("weight_optimization_allowed") is False
def test_no_promotion(): assert c.get("promotion_allowed") is False
def test_no_alpha(): assert c.get("alpha_claim_allowed") is False
def test_prod_blocked(): assert c.get("production") == "BLOCKED"
