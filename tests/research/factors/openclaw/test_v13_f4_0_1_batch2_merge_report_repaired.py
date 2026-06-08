"""V13.F4.0.1 — Repaired merge report tests."""
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent.parent.parent.parent
B2 = ROOT / "runtime_reports" / "research" / "factors" / "openclaw_batch_2"
m = json.loads((B2 / "v13_f4_0_1_batch2_merge_report_repaired.json").read_text())
def test_pass_5(): assert len(m.get("pass_research_evidence_factors", [])) == 5
def test_f02_in_pass(): assert "F02" in m.get("pass_research_evidence_factors", [])
def test_f05_in_pass(): assert "F05" in m.get("pass_research_evidence_factors", [])
def test_f09_not_pass(): assert "F09" not in m.get("pass_research_evidence_factors", [])
def test_f09_violated(): assert "F09" in m.get("source_audit_contract_violated_factors", [])
def test_no_promotion(): assert m.get("ready_for_promotion_review") == []
def test_no_composite(): assert m.get("multi_factor_composite_built") is False
def test_no_alpha(): assert m.get("alpha_claim_allowed") is False
