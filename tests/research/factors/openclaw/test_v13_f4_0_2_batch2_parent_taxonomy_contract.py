"""V13.F4.0.2 — Taxonomy contract tests."""
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent.parent.parent.parent
B2 = ROOT / "runtime_reports" / "research" / "factors" / "openclaw_batch_2"
c = json.loads((B2 / "v13_f4_0_2_batch2_parent_taxonomy_contract.json").read_text())
def test_expected_7(): assert c.get("expected_lanes_from_contract") == 7
def test_canon_only(): assert c.get("canonicalization_only") is True
def test_no_alpha(): assert c.get("alpha_claim_allowed") is False
def test_prod_blocked(): assert c.get("production") == "BLOCKED"
