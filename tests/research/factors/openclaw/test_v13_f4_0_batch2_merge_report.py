"""V13.F4.0 — Merge report tests."""
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent.parent.parent.parent
B2 = ROOT / "runtime_reports" / "research" / "factors" / "openclaw_batch_2"
m = json.loads((B2 / "v13_f4_0_batch2_merge_report.json").read_text())
def test_pass_factors(): assert len(m.get("pass_research_evidence_factors", [])) > 0
def test_source_audit(): assert len(m.get("source_audit_only_completed", [])) == 4
def test_no_promotion(): assert m.get("ready_for_promotion_review") == []
def test_no_frozen_mutation(): assert m.get("frozen_candidates_mutated") is False
def test_no_composite(): assert m.get("multi_factor_composite_built") is False
def test_no_alpha(): assert m.get("alpha_claim_allowed") is False
