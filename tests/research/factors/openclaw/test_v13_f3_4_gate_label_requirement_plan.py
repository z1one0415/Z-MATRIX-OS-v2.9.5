"""V13.F3.4 — Gate label tests."""
import json
from pathlib import Path
B = Path(__file__).resolve().parent.parent.parent.parent.parent / "runtime_reports" / "research" / "factors" / "openclaw_batch"
p = json.loads((B / "v13_f3_4_gate_label_requirement_plan.json").read_text())
def test_3_gates(): assert len(p.get("gates", [])) == 3
def test_regime_gate(): assert any(g["gate_id"]=="REGIME_GATE_FOR_F10" for g in p["gates"])
def test_cost_gate(): assert any(g["gate_id"]=="COST_TURNOVER_GATE_FOR_F11" for g in p["gates"])
def test_no_lookahead(): g = [g for g in p["gates"] if g["gate_id"]=="REGIME_GATE_FOR_F10"]; assert g and g[0].get("lookahead_regime_label_forbidden") is True
def test_no_future_cost(): g = [g for g in p["gates"] if g["gate_id"]=="COST_TURNOVER_GATE_FOR_F11"]; assert g and g[0].get("future_cost_estimate_forbidden") is True
def test_not_executed(): assert p.get("gate_execution_allowed_this_round") is False
def test_no_alpha(): assert p.get("alpha_claim_allowed") is False
