"""V13.F3.2 — Guardrails tests."""
import json
from pathlib import Path
B = Path(__file__).resolve().parent.parent.parent.parent.parent / "runtime_reports" / "research" / "factors" / "openclaw_batch"
r = json.loads((B / "v13_f3_2_freeze_risk_guardrail_registry.json").read_text())
def test_3_guardrails(): assert len(r.get("guardrails", [])) == 3
def test_f04_guardrail(): g = [g for g in r["guardrails"] if g["factor_id"]=="F04"]; assert g and g[0]["guardrail_type"]=="FULL_HORIZON_RESEARCH_ONLY"
def test_f10_regime_gate(): g = [g for g in r["guardrails"] if g["factor_id"]=="F10"]; assert g and g[0].get("requires_regime_gate") is True
def test_f11_cost_gate(): g = [g for g in r["guardrails"] if g["factor_id"]=="F11"]; assert g and g[0].get("requires_cost_gate") is True
def test_f11_turnover(): g = [g for g in r["guardrails"] if g["factor_id"]=="F11"]; assert g and g[0].get("requires_turnover_monitoring") is True
def test_all_oos(): assert all(g.get("requires_oos_before_promotion") is True for g in r["guardrails"])
def test_no_composite(): assert r.get("multi_factor_composite_built") is False
