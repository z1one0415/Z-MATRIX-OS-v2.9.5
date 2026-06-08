"""V13.F3.1 — Overlap/correlation tests."""
import json
from pathlib import Path
BATCH = Path(__file__).resolve().parent.parent.parent.parent.parent / "runtime_reports" / "research" / "factors" / "openclaw_batch"
r = json.loads((BATCH / "v13_f3_1_factor_overlap_correlation_review.json").read_text())
def test_matrix_built(): assert r.get("correlation_matrix_built") is True
def test_diversified(): assert len(r.get("diversified_candidate_set", [])) == 3
def test_no_excluded(): assert r.get("excluded_due_to_overlap") == []
def test_no_composite(): assert r.get("multi_factor_composite_built") is False
def test_no_alpha(): assert r.get("alpha_claim_allowed") is False
