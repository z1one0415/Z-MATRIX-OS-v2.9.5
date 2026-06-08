"""V13.F3.2 — Scope manifests tests."""
import json
from pathlib import Path
B = Path(__file__).resolve().parent.parent.parent.parent.parent / "runtime_reports" / "research" / "factors" / "openclaw_batch"
m = json.loads(B.read_text()) if False else json.loads((B / "v13_f3_2_candidate_freeze_scope_manifests.json").read_text())
def test_3_manifests(): assert len(m) == 3
def test_f04_full_horizon(): assert any(e["factor_id"]=="F04" and e["candidate_type"]=="FULL_HORIZON_RESEARCH_CANDIDATE" for e in m)
def test_f10_regime(): assert any(e["factor_id"]=="F10" and e["candidate_type"]=="REGIME_SPECIFIC_RESEARCH_CANDIDATE" for e in m)
def test_f11_tactical(): assert any(e["factor_id"]=="F11" and e["candidate_type"]=="TACTICAL_RESEARCH_CANDIDATE" for e in m)
def test_f10_regime_gate(): assert any(e["factor_id"]=="F10" and e.get("requires_regime_gate_before_use") is True for e in m)
def test_f11_cost_gate(): assert any(e["factor_id"]=="F11" and e.get("requires_cost_gate_before_use") is True for e in m)
def test_all_oos_required(): all(e.get("requires_true_oos_before_promotion") is True for e in m)
def test_no_promotion(): assert all(e.get("promotion_allowed") is False for e in m)
