"""V13.F3.0.2 — After-repair child audit tests."""
import json
from pathlib import Path
BATCH = Path(__file__).resolve().parent.parent.parent.parent.parent / "runtime_reports" / "research" / "factors" / "openclaw_batch"
a = json.loads((BATCH / "v13_f3_0_2_child_evidence_after_repair_audit.json").read_text())
def test_audit_8(): assert a.get("audited_factor_count") == 8
def test_inconsistent_0(): assert a.get("after_repair_inconsistent_factor_count") == 0
def test_pass_3(): assert len(a.get("pass_research_evidence_factors", [])) == 3
def test_f04_pass(): assert "F04" in a.get("pass_research_evidence_factors", [])
def test_f10_pass(): assert "F10" in a.get("pass_research_evidence_factors", [])
def test_f11_pass(): assert "F11" in a.get("pass_research_evidence_factors", [])
def test_f04_consistent(): pf = [f for f in a.get("per_factor", []) if f["factor_id"] == "F04"]; assert pf and pf[0]["after_repair_consistent"] is True
def test_f10_consistent(): pf = [f for f in a.get("per_factor", []) if f["factor_id"] == "F10"]; assert pf and pf[0]["after_repair_consistent"] is True
def test_f11_consistent(): pf = [f for f in a.get("per_factor", []) if f["factor_id"] == "F11"]; assert pf and pf[0]["after_repair_consistent"] is True
def test_hypothesis_F03R(): assert "F03R" in a.get("hypothesis_only_factors", [])
def test_blocked_4(): assert len(a.get("blocked_by_sample_factors", [])) == 4
def test_resolved_path(): pf = [f for f in a.get("per_factor", []) if f["factor_id"] == "F04"]; assert "recomputed" in pf[0].get("resolved_closeout_path", "")
