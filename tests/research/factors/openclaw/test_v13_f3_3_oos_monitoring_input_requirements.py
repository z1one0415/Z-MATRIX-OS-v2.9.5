"""V13.F3.3 — OOS/monitoring requirements tests."""
import json
from pathlib import Path
B = Path(__file__).resolve().parent.parent.parent.parent.parent / "runtime_reports" / "research" / "factors" / "openclaw_batch"
r = json.loads((B / "v13_f3_3_oos_monitoring_input_requirements.json").read_text())
def test_min_oos_6(): assert r.get("minimum_true_oos_months_required") == 6
def test_pref_oos_12(): assert r.get("preferred_true_oos_months_required") == 12
def test_no_same_promo(): assert "same_sample_promotion" in r.get("forbidden", [])
def test_no_lookahead(): assert "lookahead_regime_label" in r.get("forbidden", [])
def test_no_future_cost(): assert "future_cost_estimate" in r.get("forbidden", [])
def test_no_leakage(): assert "feature_label_leakage" in r.get("forbidden", [])
def test_no_alpha(): assert r.get("alpha_claim_allowed") is False
def test_prod_blocked(): assert r.get("production") == "BLOCKED"
