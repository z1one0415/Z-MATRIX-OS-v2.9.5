"""V13.F3.4 — Contract tests."""
import json
from pathlib import Path
B = Path(__file__).resolve().parent.parent.parent.parent.parent / "runtime_reports" / "research" / "factors" / "openclaw_batch"
c = json.loads((B / "v13_f3_4_true_oos_requirement_contract.json").read_text())
def test_plan_only(): assert c.get("requirement_plan_only") is True
def test_no_oos_exec(): assert c.get("true_oos_validation_executed") is False
def test_no_label_gen(): assert c.get("oos_label_generation_executed") is False
def test_min_6(): assert c.get("minimum_true_oos_months_required") == 6
def test_pref_12(): assert c.get("preferred_true_oos_months_required") == 12
def test_no_same_promo(): assert c.get("same_sample_promotion_forbidden") is True
def test_no_alpha(): assert c.get("alpha_claim_allowed") is False
def test_prod_blocked(): assert c.get("production") == "BLOCKED"
