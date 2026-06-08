"""V13.F3.0.1 — Recomputed child closeout tests."""
import json
from pathlib import Path

BATCH = Path(__file__).resolve().parent.parent.parent.parent.parent / "runtime_reports" / "research" / "factors" / "openclaw_batch"

def load_rc(fid):
    p = BATCH / fid / f"{fid.lower()}_closeout_recomputed.json"
    return json.loads(p.read_text()) if p.exists() else {}

def test_f04_recomputed_exists():
    assert load_rc("F04").get("factor_id") == "F04"

def test_f10_recomputed_exists():
    assert load_rc("F10").get("factor_id") == "F10"

def test_f11_recomputed_exists():
    assert load_rc("F11").get("factor_id") == "F11"

def test_f04_no_coverage_fail_pass():
    rc = load_rc("F04")
    assert not (rc.get("coverage_passed") is False and rc.get("evidence_score") == "PASS_RESEARCH_EVIDENCE")

def test_f10_no_coverage_fail_pass():
    rc = load_rc("F10")
    assert not (rc.get("coverage_passed") is False and rc.get("evidence_score") == "PASS_RESEARCH_EVIDENCE")

def test_f11_no_coverage_fail_pass():
    rc = load_rc("F11")
    assert not (rc.get("coverage_passed") is False and rc.get("evidence_score") == "PASS_RESEARCH_EVIDENCE")

def test_f04_recomputed():
    assert load_rc("F04").get("recomputed_from_artifacts") is True

def test_f10_recomputed():
    assert load_rc("F10").get("recomputed_from_artifacts") is True

def test_f11_recomputed():
    assert load_rc("F11").get("recomputed_from_artifacts") is True

def test_f04_alpha_blocked():
    assert load_rc("F04").get("alpha_claim_allowed") is False

def test_f04_prod_blocked():
    assert load_rc("F04").get("production") == "BLOCKED"
