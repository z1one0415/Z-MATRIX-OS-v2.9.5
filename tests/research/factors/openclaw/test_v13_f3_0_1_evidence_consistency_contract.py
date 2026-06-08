"""V13.F3.0.1 — Consistency contract tests."""
import json
from pathlib import Path

BATCH = Path(__file__).resolve().parent.parent.parent.parent.parent / "runtime_reports" / "research" / "factors" / "openclaw_batch"

def load(name):
    p = BATCH / name
    return json.loads(p.read_text()) if p.exists() else {}

c = load("v13_f3_0_1_evidence_consistency_contract.json")

def test_contract_built():
    assert c.get("status") == "V13_F3_0_1_EVIDENCE_CONSISTENCY_CONTRACT_BUILT"

def test_repair_only():
    assert c.get("repair_only") is True

def test_target_factors():
    assert c.get("target_factors") == ["F04", "F10", "F11"]

def test_coverage_fail_blocks_pass():
    assert c.get("coverage_fail_blocks_pass") is True

def test_parent_must_recompute():
    assert c.get("parent_merge_must_recompute_evidence_from_child_artifacts") is True

def test_alpha_false():
    assert c.get("alpha_claim_allowed") is False

def test_prod_blocked():
    assert c.get("production") == "BLOCKED"
