"""V13.F3.2 — Contract tests."""
import json
from pathlib import Path
B = Path(__file__).resolve().parent.parent.parent.parent.parent / "runtime_reports" / "research" / "factors" / "openclaw_batch"
c = json.loads((B / "v13_f3_2_candidate_freeze_review_contract.json").read_text())
def test_scope(): assert c.get("freeze_review_scope") == ["F04", "F10", "F11"]
def test_no_promotion(): assert c.get("promotion_allowed") is False
def test_no_composite(): assert c.get("multi_factor_composite_allowed") is False
def test_no_alpha(): assert c.get("alpha_claim_allowed") is False
def test_prod_blocked(): assert c.get("production") == "BLOCKED"
