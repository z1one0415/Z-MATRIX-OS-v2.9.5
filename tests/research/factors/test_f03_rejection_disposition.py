"""V13.F2.3.1 — Stage B: F03 rejection disposition tests."""
import json
from tests._path_utils import RUNTIME_FACTORS

def L(name):
    p = RUNTIME_FACTORS / name
    return json.loads(p.read_text()) if p.exists() else {}

d = L("f03_industry_relative_strength_rejection_disposition.json")

def test_disposition_built():
    assert d.get("status") == "F03_REJECTION_DISPOSITION_BUILT"

def test_factor_id():
    assert d.get("factor_id") == "F03"

def test_previous_evidence():
    assert d.get("previous_evidence_score") == "REJECTED"

def test_sample_count():
    assert d.get("sample_month_count") == 20

def test_current_direction_rejected():
    assert d.get("current_direction_rejected") is True

def test_promotion_review_blocked():
    assert d.get("promotion_review_allowed") is False

def test_multi_composite_blocked():
    assert d.get("multi_factor_composite_allowed") is False

def test_dominant_failure():
    assert d.get("dominant_failure_mode") == "DIRECTIONAL_HYPOTHESIS_REVERSAL"

def test_next_action():
    assert "REVERSAL" in d.get("recommended_next_action", "").upper()

def test_alpha_false():
    assert d.get("alpha_claim_allowed") is False

def test_prod_blocked():
    assert d.get("production") == "BLOCKED"
