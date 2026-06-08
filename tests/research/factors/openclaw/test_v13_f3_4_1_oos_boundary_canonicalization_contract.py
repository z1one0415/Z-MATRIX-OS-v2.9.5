"""V13.F3.4.1 — Contract tests."""
import json
from pathlib import Path
B = Path(__file__).resolve().parent.parent.parent.parent.parent / "runtime_reports" / "research" / "factors" / "openclaw_batch"
c = json.loads((B / "v13_f3_4_1_oos_boundary_canonicalization_contract.json").read_text())
def test_canon_only(): assert c.get("canonicalization_only") is True
def test_na_not_allowed(): assert c.get("na_last_in_sample_date_allowed") is False
def test_no_oos(): assert c.get("true_oos_validation_executed") is False
def test_no_alpha(): assert c.get("alpha_claim_allowed") is False
def test_prod_blocked(): assert c.get("production") == "BLOCKED"
