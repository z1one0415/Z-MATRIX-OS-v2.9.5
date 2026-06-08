"""V13.F3.2 — Roadmap tests."""
import json
from pathlib import Path
B = Path(__file__).resolve().parent.parent.parent.parent.parent / "runtime_reports" / "research" / "factors" / "openclaw_batch"
r = json.loads((B / "v13_f3_2_post_freeze_roadmap.json").read_text())
def test_roadmap_built(): assert r.get("status") == "V13_F3_2_POST_FREEZE_ROADMAP_BUILT"
def test_3_steps(): assert len(r.get("next_allowed_steps", [])) >= 3
def test_composite_design_allowed(): assert r.get("multi_factor_composite_design_allowed") is True
def test_composite_exec_blocked(): assert r.get("multi_factor_composite_execution_allowed") is False
def test_weight_blocked(): assert r.get("weight_optimization_allowed") is False
def test_alpha_blocked(): assert r.get("alpha_claim_allowed") is False
def test_forbidden_production(): assert "PRODUCTION" in r.get("forbidden_next_steps", [])
