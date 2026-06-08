"""V13.F3.1 — Evidence packages tests."""
import json
from pathlib import Path
BATCH = Path(__file__).resolve().parent.parent.parent.parent.parent / "runtime_reports" / "research" / "factors" / "openclaw_batch"
r = json.loads((BATCH / "v13_f3_1_candidate_evidence_packages.json").read_text())
def test_packages_built(): assert "BUILT" in r.get("status", "")
def test_3_packages(): assert len(r.get("evidence_packages", [])) == 3
def test_f04(): assert any(p["factor_id"]=="F04" for p in r["evidence_packages"])
def test_f10(): assert any(p["factor_id"]=="F10" for p in r["evidence_packages"])
def test_f11(): assert any(p["factor_id"]=="F11" for p in r["evidence_packages"])
def test_not_just_closeout(): p = next(p for p in r["evidence_packages"] if p["factor_id"]=="F04"); assert p.get("coverage_passed") is not None
def test_coverage_pass(): p = next(p for p in r["evidence_packages"] if p["factor_id"]=="F04"); assert p.get("coverage_passed") is True
def test_coverage_tier(): p = next(p for p in r["evidence_packages"] if p["factor_id"]=="F04"); assert p.get("coverage_tier") == "U475"
def test_known_risks(): p = next(p for p in r["evidence_packages"] if p["factor_id"]=="F04"); assert isinstance(p.get("known_risks"), list)
def test_no_alpha(): assert r.get("alpha_claim_allowed") is False
def test_prod_blocked(): assert r.get("production") == "BLOCKED"
