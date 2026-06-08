"""V13.F4.0.2 — Lane vs factor count tests."""
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent.parent.parent.parent
B2 = ROOT / "runtime_reports" / "research" / "factors" / "openclaw_batch_2"
a = json.loads((B2 / "v13_f4_0_2_batch2_lane_vs_factor_count_audit.json").read_text())
def test_expected_7(): assert a.get("expected_lanes_from_contract") == 7
def test_completed_7(): assert a.get("completed_lanes_detected") == 7
def test_artifacts_10(): assert a.get("factor_level_artifact_count") == 10
def test_consistent(): assert a.get("lane_count_consistency_passed") is True
def test_no_alpha(): assert a.get("alpha_claim_allowed") is False
