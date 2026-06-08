"""V13.F3.1 — Horizon/regime tests."""
import json
from pathlib import Path
BATCH = Path(__file__).resolve().parent.parent.parent.parent.parent / "runtime_reports" / "research" / "factors" / "openclaw_batch"
r = json.loads((BATCH / "v13_f3_1_horizon_regime_review.json").read_text())
def test_reviewed_3(): assert r.get("reviewed_factors") == ["F04", "F10", "F11"]
def test_per_factor_3(): assert len(r.get("per_factor_horizon_regime", [])) == 3
def test_f10_regime(): assert "F10" in r.get("regime_specific_candidates", [])
def test_f11_horizon(): assert "F11" in r.get("horizon_specific_candidates", [])
def test_f04_full(): assert "F04" in r.get("full_horizon_candidates", [])
def test_no_alpha(): assert r.get("alpha_claim_allowed") is False
