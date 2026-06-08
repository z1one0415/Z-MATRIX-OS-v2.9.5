"""V13.F4.0.1 — Repair contract tests."""
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent.parent.parent.parent
B2 = ROOT / "runtime_reports" / "research" / "factors" / "openclaw_batch_2"
c = json.loads((B2 / "v13_f4_0_1_batch2_repair_contract.json").read_text())
def test_repair_only(): assert c.get("repair_only") is True
def test_cov_fail_block(): assert c.get("coverage_fail_blocks_pass") is True
def test_source_audit_materialization_forbidden(): assert c.get("source_audit_only_materialization_forbidden") is True
def test_must_recompute(): assert c.get("parent_merge_must_recompute_from_child_artifacts") is True
def test_no_alpha(): assert c.get("alpha_claim_allowed") is False
def test_prod_blocked(): assert c.get("production") == "BLOCKED"
