"""V13.F3.2 — Freeze registry tests."""
import json
from pathlib import Path
B = Path(__file__).resolve().parent.parent.parent.parent.parent / "runtime_reports" / "research" / "factors" / "openclaw_batch"
r = json.loads((B / "v13_f3_2_candidate_freeze_registry.json").read_text())
def test_3_frozen(): assert r.get("frozen_candidate_count") == 3
def test_f04_frozen(): f = [f for f in r["frozen_candidates"] if f["factor_id"]=="F04"]; assert f and f[0]["freeze_status"]=="FROZEN_CANDIDATE"
def test_f10_frozen(): f = [f for f in r["frozen_candidates"] if f["factor_id"]=="F10"]; assert f and f[0]["freeze_status"]=="FROZEN_CANDIDATE"
def test_f11_tactical(): f = [f for f in r["frozen_candidates"] if f["factor_id"]=="F11"]; assert f and "TACTICAL" in f[0]["freeze_status"]
def test_ready_3_3(): assert "F04" in r.get("ready_for_f3_3_research_composite_design", [])
def test_no_promotion(): assert r.get("ready_for_promotion_review") == []
def test_no_composite(): assert r.get("multi_factor_composite_built") is False
def test_no_alpha(): assert r.get("alpha_claim_allowed") is False
