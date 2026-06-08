"""V13.F4.0 — Selection scorecard tests."""
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent.parent.parent.parent
B2 = ROOT / "runtime_reports" / "research" / "factors" / "openclaw_batch_2"
s = json.loads((B2 / "v13_f4_0_batch2_factor_selection_scorecard.json").read_text())
def test_registry_selection(): assert s.get("selection_scope_from_registry") is True
def test_has_lanes(): assert len(s.get("selected_batch2_lanes", [])) >= 7
def test_frozen_overlap_blocked(): assert s.get("frozen_candidate_overlap_blocked") is True
def test_no_alpha(): assert s.get("alpha_claim_allowed") is False
