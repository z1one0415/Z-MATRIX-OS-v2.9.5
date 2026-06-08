"""V13.F2.3 — Stage G: evidence scorecard tests."""
import json
from tests._path_utils import RUNTIME_FACTORS

def L(name):
    p = RUNTIME_FACTORS / name
    return json.loads(p.read_text()) if p.exists() else {}

sc = L("v13_f2_3_single_factor_evidence_scorecard.json")

def test_scorecard_built():
    assert sc.get("status") == "V13_F2_3_SINGLE_FACTOR_EVIDENCE_SCORECARD_BUILT"

def test_validated_factors():
    assert sc.get("validated_factors") == ["F03", "F06"]

def test_validation_executed():
    assert sc.get("single_factor_validation_executed") is True

def test_per_factor_count():
    assert len(sc.get("per_factor_evidence_scorecard", [])) == 2

def test_f03_has_score():
    f03 = next((f for f in sc.get("per_factor_evidence_scorecard", []) if f["factor_id"] == "F03"), None)
    assert f03 is not None
    assert f03.get("evidence_score") in (
        "PASS_RESEARCH_EVIDENCE", "TACTICAL_ONLY", "WEAK_OR_UNSTABLE",
        "BLOCKED_BY_INSUFFICIENT_SAMPLE", "REJECTED"
    )

def test_f06_has_score():
    f06 = next((f for f in sc.get("per_factor_evidence_scorecard", []) if f["factor_id"] == "F06"), None)
    assert f06 is not None
    assert f06.get("evidence_score") in (
        "PASS_RESEARCH_EVIDENCE", "TACTICAL_ONLY", "WEAK_OR_UNSTABLE",
        "BLOCKED_BY_INSUFFICIENT_SAMPLE", "REJECTED"
    )

def test_f03_sample_count():
    f03 = next((f for f in sc.get("per_factor_evidence_scorecard", []) if f["factor_id"] == "F03"), None)
    assert f03.get("sample_month_count", 0) > 0

def test_f03_has_rationale():
    f03 = next((f for f in sc.get("per_factor_evidence_scorecard", []) if f["factor_id"] == "F03"), None)
    assert len(f03.get("rationale", "")) > 0

def test_count_fields():
    total = sc.get("factor_pass_count", 0) + sc.get("factor_tactical_count", 0) + \
            sc.get("factor_blocked_count", 0) + sc.get("factor_rejected_count", 0) + \
            sc.get("factor_weak_count", 0)
    assert total == 2

def test_alpha_false():
    assert sc.get("alpha_claim_allowed") is False

def test_v13_6_false():
    assert sc.get("v13_6_allowed") is False

def test_prod_blocked():
    assert sc.get("production") == "BLOCKED"
