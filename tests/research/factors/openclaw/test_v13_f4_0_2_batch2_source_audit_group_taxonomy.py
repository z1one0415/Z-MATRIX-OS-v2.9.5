"""V13.F4.0.2 — Source audit group taxonomy tests."""
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent.parent.parent.parent
B2 = ROOT / "runtime_reports" / "research" / "factors" / "openclaw_batch_2"
a = json.loads((B2 / "v13_f4_0_2_batch2_source_audit_group_taxonomy_audit.json").read_text())
def test_group_status(): assert "COMPLETED" in a.get("group_status", "")
def test_all_clean(): assert a.get("all_members_source_audit_clean") is True
def test_not_coverage_blocked(): assert a.get("group_must_not_be_coverage_blocked") is True
def test_4_members(): assert len(a.get("source_audit_group_members", [])) == 4
def test_no_alpha(): assert a.get("alpha_claim_allowed") is False
