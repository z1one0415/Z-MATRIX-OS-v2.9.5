"""V13.F3.3 — Role architecture tests."""
import json
from pathlib import Path
B = Path(__file__).resolve().parent.parent.parent.parent.parent / "runtime_reports" / "research" / "factors" / "openclaw_batch"
r = json.loads((B / "v13_f3_3_composite_role_architecture.json").read_text())
def test_3_factors(): assert len(r.get("component_factors", [])) == 3
def test_f04_core(): f = [f for f in r["component_factors"] if f["factor_id"]=="F04"]; assert f and f[0]["role"]=="CORE_SIGNAL"
def test_f10_regime_gate(): f = [f for f in r["component_factors"] if f["factor_id"]=="F10"]; assert f and f[0].get("required_gate")=="REGIME_GATE"
def test_f11_cost_gate(): f = [f for f in r["component_factors"] if f["factor_id"]=="F11"]; assert f and f[0].get("required_gate")=="COST_TURNOVER_GATE"
def test_no_weights(): assert r.get("numeric_weights_assigned") is False
def test_no_panel(): assert r.get("composite_panel_generated") is False
def test_no_composite(): assert r.get("multi_factor_composite_built") is False
def test_no_alpha(): assert r.get("alpha_claim_allowed") is False
def test_prod_blocked(): assert r.get("production") == "BLOCKED"
