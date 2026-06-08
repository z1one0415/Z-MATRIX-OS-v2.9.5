"""V13.F3.1 — Scorecard tests."""
import json
from pathlib import Path
BATCH = Path(__file__).resolve().parent.parent.parent.parent.parent / "runtime_reports" / "research" / "factors" / "openclaw_batch"
sc = json.loads((BATCH / "v13_f3_1_candidate_review_scorecard.json").read_text())
def test_3_decision(): assert len(sc.get("per_factor_candidate_decision", [])) == 3
def test_f04_decision(): d = [d for d in sc["per_factor_candidate_decision"] if d["factor_id"]=="F04"]; assert d and d[0]["decision"] in ("FREEZE_CANDIDATE","TACTICAL_CANDIDATE","REGIME_SPECIFIC_CANDIDATE","HORIZON_SPECIFIC_CANDIDATE","NEEDS_OOS","REWORK_REQUIRED","REJECTED")
def test_f10_decision(): d = [d for d in sc["per_factor_candidate_decision"] if d["factor_id"]=="F10"]; assert d and d[0]["decision"] in ("FREEZE_CANDIDATE","TACTICAL_CANDIDATE","REGIME_SPECIFIC_CANDIDATE","HORIZON_SPECIFIC_CANDIDATE","NEEDS_OOS","REWORK_REQUIRED","REJECTED")
def test_f11_decision(): d = [d for d in sc["per_factor_candidate_decision"] if d["factor_id"]=="F11"]; assert d and d[0]["decision"] in ("FREEZE_CANDIDATE","TACTICAL_CANDIDATE","REGIME_SPECIFIC_CANDIDATE","HORIZON_SPECIFIC_CANDIDATE","NEEDS_OOS","REWORK_REQUIRED","REJECTED")
def test_no_promotion(): assert sc.get("ready_for_promotion_review") == []
def test_f3_2_list(): assert isinstance(sc.get("ready_for_f3_2_candidate_freeze_review"), list)
def test_no_composite(): assert sc.get("multi_factor_composite_built") is False
def test_no_alpha(): assert sc.get("alpha_claim_allowed") is False
def test_prod_blocked(): assert sc.get("production") == "BLOCKED"
