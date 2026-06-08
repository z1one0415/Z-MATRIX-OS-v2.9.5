"""V13.F4.0.2 — Canonical merge tests."""
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent.parent.parent.parent
B2 = ROOT / "runtime_reports" / "research" / "factors" / "openclaw_batch_2"
m = json.loads((B2 / "v13_f4_0_2_batch2_merge_report_canonical.json").read_text())
def test_7_lanes(): assert m.get("expected_lanes_from_contract") == 7 and m.get("completed_lanes_detected") == 7
def test_consistent(): assert m.get("lane_count_consistency_passed") is True
def test_pass_5(): assert len(m.get("pass_research_evidence_factors", [])) == 5
def test_f09_violated(): assert m.get("source_audit_contract_violated_factors") == ["F09"]
def test_f17_group(): assert "F17_F20_GROUP" in m.get("source_audit_group_completed", [])
def test_no_coverage_blocked(): assert m.get("materialized_but_coverage_blocked_factors") == []
def test_no_promotion(): assert m.get("ready_for_promotion_review") == []
def test_no_composite(): assert m.get("multi_factor_composite_built") is False
def test_no_alpha(): assert m.get("alpha_claim_allowed") is False
