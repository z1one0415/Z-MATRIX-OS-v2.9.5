"""V13.F3.0.1 — Merge report tests."""
import json
from pathlib import Path

BATCH = Path(__file__).resolve().parent.parent.parent.parent.parent / "runtime_reports" / "research" / "factors" / "openclaw_batch"

def load(name):
    p = BATCH / name
    return json.loads(p.read_text()) if p.exists() else {}

m = load("v13_f3_0_1_parallel_batch_merge_report.json")

def test_merge_repaired():
    assert "REPAIRED" in m.get("status", "")

def test_evidence_consistency_passed():
    assert m.get("evidence_consistency_passed") is True

def test_coverage_consistency_passed():
    assert m.get("coverage_consistency_passed") is True

def test_ready_next_does_not_include_coverage_fail():
    ready = m.get("ready_for_next_validation", [])
    cov_blocked = m.get("materialized_but_coverage_blocked_factors", [])
    for f in ready:
        assert f not in cov_blocked

def test_promotion_empty():
    assert m.get("ready_for_promotion_review") == []

def test_multi_composite_false():
    assert m.get("multi_factor_composite_built") is False

def test_v13_6_false():
    assert m.get("v13_6_allowed") is False

def test_alpha_false():
    assert m.get("alpha_claim_allowed") is False

def test_prod_blocked():
    assert m.get("production") == "BLOCKED"
