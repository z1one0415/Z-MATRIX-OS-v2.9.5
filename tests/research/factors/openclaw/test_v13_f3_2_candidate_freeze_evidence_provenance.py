"""V13.F3.2 — Evidence provenance tests."""
import json
from pathlib import Path
B = Path(__file__).resolve().parent.parent.parent.parent.parent / "runtime_reports" / "research" / "factors" / "openclaw_batch"
a = json.loads((B / "v13_f3_2_candidate_freeze_evidence_provenance_audit.json").read_text())
def test_3_audited(): assert len(a.get("audited_factors", [])) == 3
def test_pass(): assert "PASS" in a.get("status", "")
def test_valid_3(): assert a.get("provenance_passed_factor_count") == 3
def test_blocked_0(): assert a.get("provenance_blocked_factor_count") == 0
def test_u475(): assert a.get("all_coverage_u475") is True
def test_pit(): assert a.get("all_pit_passed") is True
def test_sources(): assert a.get("all_candidate_sources_valid") is True
