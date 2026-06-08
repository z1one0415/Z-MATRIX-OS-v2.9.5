"""V13.F3.0.2 — Canonical merge report tests."""
import json
from pathlib import Path
BATCH = Path(__file__).resolve().parent.parent.parent.parent.parent / "runtime_reports" / "research" / "factors" / "openclaw_batch"
m = json.loads((BATCH / "v13_f3_0_2_parallel_batch_merge_report.json").read_text())
def test_status(): assert "PASS" in m.get("status", "")
def test_pass_3(): assert len(m.get("pass_research_evidence_factors", [])) == 3
def test_ready_next(): assert m.get("ready_for_next_validation") == ["F04", "F10", "F11"]
def test_hypothesis(): assert "F03R" in m.get("hypothesis_only_factors", [])
def test_blocked(): assert len(m.get("blocked_by_sample_factors", [])) == 4
def test_evidence_consistent(): assert m.get("after_repair_evidence_consistency_passed") is True
def test_coverage_consistent(): assert m.get("after_repair_coverage_consistency_passed") is True
def test_promotion_empty(): assert m.get("ready_for_promotion_review") == []
def test_prod_blocked(): assert m.get("production") == "BLOCKED"
