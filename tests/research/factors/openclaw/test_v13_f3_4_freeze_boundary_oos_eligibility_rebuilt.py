"""V13.F3.4 — Rebuilt freeze boundary tests."""
import json
from pathlib import Path
B = Path(__file__).resolve().parent.parent.parent.parent.parent / "runtime_reports" / "research" / "factors" / "openclaw_batch"
p = json.loads((B / "v13_f3_4_freeze_boundary_oos_eligibility_plan.json").read_text())
def test_all_resolved(): assert p.get("all_last_in_sample_dates_resolved") is True
def test_no_na(): assert p.get("any_na_last_in_sample_date") is False
def test_oos_start(): assert len(p.get("minimum_oos_start_exclusive", "")) > 0
def test_no_oos(): assert p.get("true_oos_validation_executed") is False
def test_no_alpha(): assert p.get("alpha_claim_allowed") is False
def test_prod_blocked(): assert p.get("production") == "BLOCKED"
