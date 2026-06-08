"""V13.F3.4 — OOS calendar tests."""
import json
from pathlib import Path
B = Path(__file__).resolve().parent.parent.parent.parent.parent / "runtime_reports" / "research" / "factors" / "openclaw_batch"
p = json.loads((B / "v13_f3_4_oos_calendar_requirement_plan.json").read_text())
def test_min_6(): assert p.get("minimum_true_oos_rebalance_months_required") == 6
def test_pref_12(): assert p.get("preferred_true_oos_rebalance_months_required") == 12
def test_coverage_u475(): assert p.get("minimum_cross_section_coverage_tier") == "U475"
def test_not_generated(): assert p.get("oos_calendar_generation_executed") is False
def test_no_alpha(): assert p.get("alpha_claim_allowed") is False
def test_prod_blocked(): assert p.get("production") == "BLOCKED"
