"""V13.F3.4 — Same-sample block tests."""
import json
from pathlib import Path
B = Path(__file__).resolve().parent.parent.parent.parent.parent / "runtime_reports" / "research" / "factors" / "openclaw_batch"
a = json.loads((B / "v13_f3_4_same_sample_promotion_block_audit.json").read_text())
def test_blocked(): assert a.get("same_sample_promotion_blocked") is True
def test_promotion_empty(): assert a.get("ready_for_promotion_review") == []
def test_no_oos(): assert a.get("true_oos_validation_executed") is False
def test_no_composite(): assert a.get("composite_execution_executed") is False
def test_no_alpha(): assert a.get("alpha_claim_allowed") is False
def test_violations_0(): assert a.get("violation_count", 999) == 0
