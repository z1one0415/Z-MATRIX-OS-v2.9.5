"""V13.F3.0.3 — Taxonomy audit tests."""
import json
from pathlib import Path
BATCH = Path(__file__).resolve().parent.parent.parent.parent.parent / "runtime_reports" / "research" / "factors" / "openclaw_batch"
a = json.loads((BATCH / "v13_f3_0_3_blocked_factor_taxonomy_audit.json").read_text())

def test_inconsistent_0(): assert a.get("after_repair_inconsistent_factor_count") == 0
def test_pass_3(): assert len(a.get("pass_research_evidence_factors", [])) == 3
def test_blocked_4(): assert len(a.get("blocked_by_sample_factors", [])) == 4
def test_hyp_1(): assert len(a.get("hypothesis_only_factors", [])) == 1
def test_f04_pass(): assert "F04" in a.get("pass_research_evidence_factors", [])
def test_f10_pass(): assert "F10" in a.get("pass_research_evidence_factors", [])
def test_f11_pass(): assert "F11" in a.get("pass_research_evidence_factors", [])
def test_f12_blocked(): assert "F12" in a.get("blocked_by_sample_factors", [])
def test_f03r_hyp(): assert "F03R" in a.get("hypothesis_only_factors", [])

def test_f04_consistent(): pf = [f for f in a.get("per_factor",[]) if f["factor_id"]=="F04"]; assert pf and pf[0]["after_repair_consistent"]
def test_f10_consistent(): pf = [f for f in a.get("per_factor",[]) if f["factor_id"]=="F10"]; assert pf and pf[0]["after_repair_consistent"]
def test_f11_consistent(): pf = [f for f in a.get("per_factor",[]) if f["factor_id"]=="F11"]; assert pf and pf[0]["after_repair_consistent"]
def test_f12_consistent(): pf = [f for f in a.get("per_factor",[]) if f["factor_id"]=="F12"]; assert pf and pf[0]["after_repair_consistent"]
def test_f13_consistent(): pf = [f for f in a.get("per_factor",[]) if f["factor_id"]=="F13"]; assert pf and pf[0]["after_repair_consistent"]
def test_f07_consistent(): pf = [f for f in a.get("per_factor",[]) if f["factor_id"]=="F07"]; assert pf and pf[0]["after_repair_consistent"]
def test_f08_consistent(): pf = [f for f in a.get("per_factor",[]) if f["factor_id"]=="F08"]; assert pf and pf[0]["after_repair_consistent"]
def test_f03r_consistent(): pf = [f for f in a.get("per_factor",[]) if f["factor_id"]=="F03R"]; assert pf and pf[0]["after_repair_consistent"]

def test_f12_blocked_display(): pf = [f for f in a.get("per_factor",[]) if f["factor_id"]=="F12"]; assert pf and pf[0]["display_evidence_score"] == "BLOCKED_BY_SAMPLE"
def test_f12_canonical(): pf = [f for f in a.get("per_factor",[]) if f["factor_id"]=="F12"]; assert pf and "COVERAGE" in pf[0]["canonical_evidence_score"]

def test_taxonomy_pass(): assert a.get("taxonomy_consistency_passed") is True
def test_alpha_false(): assert a.get("alpha_claim_allowed") is False
def test_prod_blocked(): assert a.get("production") == "BLOCKED"
