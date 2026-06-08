"""V13.F2.3.1 — Stage D: F06 insufficient sample disposition tests."""
import json
from tests._path_utils import RUNTIME_FACTORS

def L(name):
    p = RUNTIME_FACTORS / name
    return json.loads(p.read_text()) if p.exists() else {}

d = L("f06_fundamental_quality_insufficient_sample_disposition.json")

def test_disposition_built():
    assert d.get("status") == "F06_INSUFFICIENT_SAMPLE_DISPOSITION_BUILT"

def test_factor_id():
    assert d.get("factor_id") == "F06"

def test_previous_evidence():
    assert d.get("previous_evidence_score") == "BLOCKED_BY_INSUFFICIENT_SAMPLE"

def test_sample_count():
    assert d.get("sample_month_count") == 1

def test_not_rejected():
    assert d.get("factor_rejected") is False

def test_not_promoted():
    assert d.get("factor_promoted") is False

def test_validation_blocked():
    assert d.get("validation_blocked") is True

def test_blocked_reason():
    assert "INSUFFICIENT" in d.get("blocked_reason", "")

def test_minimum_count():
    assert d.get("minimum_month_count_required") == 12

def test_preferred_count():
    assert d.get("preferred_month_count_required") == 24

def test_alpha_false():
    assert d.get("alpha_claim_allowed") is False

def test_prod_blocked():
    assert d.get("production") == "BLOCKED"
