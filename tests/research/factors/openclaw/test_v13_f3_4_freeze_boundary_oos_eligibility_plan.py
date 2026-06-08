"""V13.F3.4 — Freeze boundary tests."""
import json
from pathlib import Path
B = Path(__file__).resolve().parent.parent.parent.parent.parent / "runtime_reports" / "research" / "factors" / "openclaw_batch"
p = json.loads((B / "v13_f3_4_freeze_boundary_oos_eligibility_plan.json").read_text())
def test_plan_built(): assert "FREEZE_BOUNDARY" in p.get("status", "")
def test_3_factors(): assert len(p.get("per_factor_last_in_sample_rebalance_date", [])) == 3
def test_oos_not_executed(): assert p.get("true_oos_validation_executed") is False
def test_no_alpha(): assert p.get("alpha_claim_allowed") is False
