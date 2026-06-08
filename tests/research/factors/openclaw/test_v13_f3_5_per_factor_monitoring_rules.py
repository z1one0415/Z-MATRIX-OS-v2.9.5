"""V13.F3.5 — Per-factor rules tests."""
import json
from pathlib import Path
B = Path(__file__).resolve().parent.parent.parent.parent.parent / "runtime_reports" / "research" / "factors" / "openclaw_batch"
r = json.loads((B / "v13_f3_5_per_factor_monitoring_rules.json").read_text())
def test_3_rules(): assert len(r.get("rules", [])) == 3
def test_f04_20d_60d(): ru = [x for x in r["rules"] if x["factor_id"]=="F04"]; assert ru and "20D" in ru[0]["monitoring_horizons"] and "60D" in ru[0]["monitoring_horizons"]
def test_f10_gate(): ru = [x for x in r["rules"] if x["factor_id"]=="F10"]; assert ru and ru[0].get("required_gate")=="REGIME_GATE_FOR_F10"
def test_f11_gate(): ru = [x for x in r["rules"] if x["factor_id"]=="F11"]; assert ru and ru[0].get("required_gate")=="COST_TURNOVER_GATE_FOR_F11"
def test_f11_blocked_60d(): ru = [x for x in r["rules"] if x["factor_id"]=="F11"]; assert ru and any(h.startswith('60D') for h in ru[0].get('blocked_horizons',[]))
def test_no_promotion(): assert all(ru.get("promotion_allowed") is False for ru in r["rules"])
def test_not_executed(): assert r.get("monitoring_execution_executed") is False
def test_no_alpha(): assert r.get("alpha_claim_allowed") is False
