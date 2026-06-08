"""V13.F3.0.3 — Taxonomy contract tests."""
import json
from pathlib import Path
BATCH = Path(__file__).resolve().parent.parent.parent.parent.parent / "runtime_reports" / "research" / "factors" / "openclaw_batch"
c = json.loads((BATCH / "v13_f3_0_3_blocked_taxonomy_contract.json").read_text())
def test_canonicalization_only(): assert c.get("canonicalization_only") is True
def test_no_rerun_mat(): assert c.get("materialization_rerun_allowed") is False
def test_no_rerun_val(): assert c.get("single_factor_validation_rerun_allowed") is False
def test_alias(): assert "COVERAGE_BLOCKED_WITH_INSUFFICIENT_SAMPLE" in c.get("blocked_display_alias_allowed", {})
def test_prod_blocked(): assert c.get("production") == "BLOCKED"
