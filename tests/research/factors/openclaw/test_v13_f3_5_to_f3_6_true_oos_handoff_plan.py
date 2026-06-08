"""V13.F3.5 — F3.6 handoff tests."""
import json
from pathlib import Path
B = Path(__file__).resolve().parent.parent.parent.parent.parent / "runtime_reports" / "research" / "factors" / "openclaw_batch"
h = json.loads((B / "v13_f3_5_to_f3_6_true_oos_handoff_plan.json").read_text())
def test_not_ready(): assert h.get("ready_for_f3_6_now") is False
def test_min_6(): assert h["handoff_allowed_only_when"].get("minimum_true_oos_months_available") == 6
def test_no_oos(): assert h.get("true_oos_validation_executed") is False
def test_no_alpha(): assert h.get("alpha_claim_allowed") is False
