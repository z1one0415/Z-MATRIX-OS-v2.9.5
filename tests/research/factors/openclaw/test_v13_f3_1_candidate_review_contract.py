"""V13.F3.1 — Contract tests."""
import json
from pathlib import Path
BATCH = Path(__file__).resolve().parent.parent.parent.parent.parent / "runtime_reports" / "research" / "factors" / "openclaw_batch"
c = json.loads((BATCH / "v13_f3_1_candidate_review_contract.json").read_text())
def test_scope(): assert c.get("candidate_review_scope") == ["F04", "F10", "F11"]
def test_review_only(): assert c.get("review_only") is True
def test_no_promotion(): assert c.get("promotion_allowed") is False
def test_no_composite(): assert c.get("multi_factor_composite_allowed") is False
def test_no_alpha(): assert c.get("alpha_claim_allowed") is False
def test_prod_blocked(): assert c.get("production") == "BLOCKED"
