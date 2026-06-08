"""V13.F4.0.1 — Coverage expansion tests."""
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent.parent.parent.parent
B2 = ROOT / "runtime_reports" / "research" / "factors" / "openclaw_batch_2"
r = json.loads((B2 / "v13_f4_0_1_batch2_coverage_expansion_repair.json").read_text())
def test_5_attempted(): assert len(r.get("coverage_expansion_attempted_factors", [])) == 5
def test_f09_forbidden(): assert "F09" in r.get("coverage_expansion_forbidden_factors", [])
def test_f02_u475(): p = [p for p in r["per_factor_coverage_repair"] if p["factor_id"]=="F02"]; assert p and p[0]["coverage_tier"]=="U475"
def test_f02_pass(): p = [p for p in r["per_factor_coverage_repair"] if p["factor_id"]=="F02"]; assert p and p[0]["coverage_passed"] is True
def test_f05_pass(): p = [p for p in r["per_factor_coverage_repair"] if p["factor_id"]=="F05"]; assert p and p[0]["coverage_passed"] is True
def test_no_alpha(): assert r.get("alpha_claim_allowed") is False
