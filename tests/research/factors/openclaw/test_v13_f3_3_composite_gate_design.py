"""V13.F3.3 — Gate design tests."""
import json
from pathlib import Path
B = Path(__file__).resolve().parent.parent.parent.parent.parent / "runtime_reports" / "research" / "factors" / "openclaw_batch"
g = json.loads((B / "v13_f3_3_composite_gate_design.json").read_text())
def test_3_gates(): assert len(g.get("gates", [])) == 3
def test_regime_gate(): assert any(gg["gate_id"]=="REGIME_GATE_FOR_F10" for gg in g["gates"])
def test_cost_gate(): assert any(gg["gate_id"]=="COST_TURNOVER_GATE_FOR_F11" for gg in g["gates"])
def test_horizon_gate(): assert any(gg["gate_id"]=="HORIZON_GATE" for gg in g["gates"])
def test_no_exec(): assert g.get("gate_execution_allowed") is False
def test_no_composite(): assert g.get("composite_execution_allowed") is False
def test_no_alpha(): assert g.get("alpha_claim_allowed") is False
