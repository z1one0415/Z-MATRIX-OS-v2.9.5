"""V13.F3.0.3 — Merge report tests."""
import json
from pathlib import Path
BATCH = Path(__file__).resolve().parent.parent.parent.parent.parent / "runtime_reports" / "research" / "factors" / "openclaw_batch"
m = json.loads((BATCH / "v13_f3_0_3_parallel_batch_merge_report.json").read_text())
def test_pass_3(): assert m.get("pass_research_evidence_factors") == ["F04", "F10", "F11"]
def test_blocked_4(): assert len(m.get("blocked_by_sample_factors", [])) == 4
def test_hyp_1(): assert m.get("hypothesis_only_factors") == ["F03R"]
def test_ready_f3_1(): assert m.get("ready_for_f3_1_candidate_review") == ["F04", "F10", "F11"]
def test_promotion_empty(): assert m.get("ready_for_promotion_review") == []
def test_taxonomy_pass(): assert m.get("taxonomy_consistency_passed") is True
def test_multi_composite_false(): assert m.get("multi_factor_composite_built") is False
def test_prod_blocked(): assert m.get("production") == "BLOCKED"
