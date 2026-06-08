"""V13.F3.4 — Per-factor criteria tests."""
import json
from pathlib import Path
B = Path(__file__).resolve().parent.parent.parent.parent.parent / "runtime_reports" / "research" / "factors" / "openclaw_batch"
p = json.loads((B / "v13_f3_4_per_factor_oos_acceptance_criteria.json").read_text())
def test_3_criteria(): assert len(p.get("criteria", [])) == 3
def test_f04_20d_60d(): c = [c for c in p["criteria"] if c["factor_id"]=="F04"]; assert c and "20D" in c[0]["required_horizons"] and "60D" in c[0]["required_horizons"]
def test_f10_gate(): c = [c for c in p["criteria"] if c["factor_id"]=="F10"]; assert c and c[0].get("required_gate")=="REGIME_GATE_FOR_F10"
def test_f11_gate(): c = [c for c in p["criteria"] if c["factor_id"]=="F11"]; assert c and c[0].get("required_gate")=="COST_TURNOVER_GATE_FOR_F11"
def test_f11_blocked_60d(): c = [c for c in p["criteria"] if c["factor_id"]=="F11"]; assert c and "60D" in "".join(c[0].get("blocked_horizons",[]))
def test_min_6(): assert all(c.get("minimum_oos_months")==6 for c in p["criteria"])
def test_pref_12(): assert all(c.get("preferred_oos_months")==12 for c in p["criteria"])
def test_not_executed(): assert p.get("oos_validation_executed") is False
def test_no_promotion(): assert p.get("promotion_allowed") is False
def test_no_alpha(): assert p.get("alpha_claim_allowed") is False
