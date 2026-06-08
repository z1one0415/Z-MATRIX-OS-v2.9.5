"""V13.F3.0.2 — Canonicalization contract tests."""
import json
from pathlib import Path
BATCH = Path(__file__).resolve().parent.parent.parent.parent.parent / "runtime_reports" / "research" / "factors" / "openclaw_batch"
c = json.loads((BATCH / "v13_f3_0_2_closeout_canonicalization_contract.json").read_text())
def test_canonicalization_only(): assert c.get("canonicalization_only") is True
def test_materialization_not_rerun(): assert c.get("materialization_rerun_allowed") is False
def test_validation_not_rerun(): assert c.get("single_factor_validation_rerun_allowed") is False
def test_prod_blocked(): assert c.get("production") == "BLOCKED"
