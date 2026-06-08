"""V13.F3.1 — Signal stability tests."""
import json
from pathlib import Path
BATCH = Path(__file__).resolve().parent.parent.parent.parent.parent / "runtime_reports" / "research" / "factors" / "openclaw_batch"
r = json.loads((BATCH / "v13_f3_1_signal_stability_review.json").read_text())
def test_reviewed_3(): assert r.get("reviewed_factors") == ["F04", "F10", "F11"]
def test_per_factor_3(): assert len(r.get("per_factor_signal_stability", [])) == 3
def test_f04_has_status(): p = next(p for p in r["per_factor_signal_stability"] if p["factor_id"]=="F04"); assert len(p.get("signal_stability_status", "")) > 0
def test_f10_has_status(): p = next(p for p in r["per_factor_signal_stability"] if p["factor_id"]=="F10"); assert len(p.get("signal_stability_status", "")) > 0
def test_f11_has_status(): p = next(p for p in r["per_factor_signal_stability"] if p["factor_id"]=="F11"); assert len(p.get("signal_stability_status", "")) > 0
def test_ic_checked(): p = next(p for p in r["per_factor_signal_stability"] if p["factor_id"]=="F04"); assert isinstance(p.get("ic_20d_direction_pass"), bool)
def test_no_alpha(): assert r.get("alpha_claim_allowed") is False
